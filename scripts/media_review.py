"""Local signal/metadata review. Measurements never certify listening or motion QA."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", check=True, timeout=600)


def sha(path):
    with Path(path).open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def number(value):
    try:
        value = float(value)
        return value if math.isfinite(value) else None
    except (ValueError, TypeError):
        return None


def aspect(width, height, target=(9, 16)):
    if width <= 0 or height <= 0 or min(target) <= 0:
        raise ValueError("Dimensions must be positive")
    error = abs((width / height) / (target[0] / target[1]) - 1)
    exact = width * target[1] == height * target[0]
    return {"width": width, "height": height, "relative_error": error,
            "exact_export": exact, "input_ratio_pass": error <= .001,
            "content_qa": "not_checked"}


def duration_check(actual, expected, fps=None):
    tolerance = max(.05, 1 / fps if fps and fps > 0 else .05)
    return {"actual": actual, "expected": expected, "tolerance": tolerance,
            "status": "not_checked" if actual is None or expected is None else
            "pass" if abs(actual - expected) <= tolerance else "fail"}


def capabilities():
    return {"executables": {x: shutil.which(x) for x in ("ffmpeg", "ffprobe", "whisperx")},
            "continuous_visual_understanding": "not_verified",
            "environment_audio_understanding": "not_verified",
            "note": "Decoder, frames and ASR do not verify native perception. Check actual session tools and coverage."}


def probe(path):
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                           "-of", "json", str(path)]).stdout)


def meter(path, target, peak, start=None, length=None):
    args = ["ffmpeg", "-hide_banner", "-nostdin", "-i", str(path)]
    if start is not None:
        args += ["-ss", str(start), "-t", str(length)]
    args += ["-map", "0:a:0", "-vn", "-af",
             f"loudnorm=I={target}:TP={peak}:LRA=11:print_format=json", "-f", "null", "-"]
    output = run(args).stderr
    data = json.loads(output[output.rfind("{"):output.rfind("}") + 1])
    return {key: number(value) for key, value in data.items()}


def audio_status(measure, target=None, peak=None):
    if measure["input_i"] is None:
        return "silent_or_unmeasurable"
    if peak is not None and measure["input_tp"] is not None and measure["input_tp"] > peak:
        return "peak_exceeded"
    if target is None:
        return "measured_without_brief_target"
    return "within_target" if abs(measure["input_i"] - target) <= 1 else "level_outside_target"


def inspect(path, expected=None, target=None, peak=None):
    path = Path(path).resolve(strict=True)
    meta = probe(path)
    video = next((s for s in meta["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in meta["streams"] if s["codec_type"] == "audio"), None)
    actual = number(video.get("duration")) if video else None
    # Container duration includes audio tails; never use it to pass a video duration check.
    fps = None
    if video:
        numerator, denominator = video.get("avg_frame_rate", "0/1").split("/")
        fps = float(numerator) / float(denominator) if float(denominator) else None
    report = {"schema": 1, "path": str(path), "sha256": sha(path),
              "duration": duration_check(actual, expected, fps),
              "container_duration": number(meta.get("format", {}).get("duration")),
              "actual_model": "unknown", "actual_interface": "unknown",
              "motion_qa": "not_checked", "listening_qa": "not_checked",
              "anatomy_qa": "not_checked", "metadata": meta}
    if video:
        report["raster"] = aspect(video["width"], video["height"])
        report["raster"]["note"] = "Encoded raster only; inspect rotation and sample aspect ratio before display QA."
    if not audio:
        report["audio"] = {"status": "no_audio"}
        return report
    # Parameters below support measurement; they are not a universal delivery target.
    measured = meter(path, target if target is not None else -24, peak if peak is not None else -2)
    audio_duration = number(audio.get("duration")) or actual or report["container_duration"]
    windows = {}
    if audio_duration:
        window = min(3., audio_duration)
        for name, start in (("head", 0), ("middle", max(0, (audio_duration-window)/2)),
                            ("tail", max(0, audio_duration-window))):
            windows[name] = meter(path, target if target is not None else -24,
                                  peak if peak is not None else -2, start, window)
    report["audio"] = {"status": audio_status(measured, target, peak), "whole": measured,
                       "windows": windows, "brief_target_lufs": target, "brief_peak_dbtp": peak,
                       "noise_source_sync": "not_checked"}
    return report


def normalize(path, output, target, peak, authorization, listening_review):
    path, output = Path(path).resolve(strict=True), Path(output).resolve()
    sidecar = Path(str(output) + ".review.json")
    if output == path or output.exists() or sidecar.exists():
        raise ValueError("Use a new versioned output; input/output must not be overwritten")
    for record in (authorization, listening_review):
        if not Path(record).is_file() or not Path(record).read_text(encoding="utf-8").strip():
            raise ValueError("Saved authorization and listening/noise assessment are required")
    before = inspect(path, target=target, peak=peak)
    if before["audio"]["status"] in ("no_audio", "silent_or_unmeasurable", "within_target"):
        raise ValueError("No normalization needed or usable signal absent")
    measured = before["audio"]["whole"]
    keys = {"measured_I": "input_i", "measured_TP": "input_tp",
            "measured_LRA": "input_lra", "measured_thresh": "input_thresh", "offset": "target_offset"}
    if any(measured[key] is None for key in keys.values()):
        raise ValueError("Non-finite measurement; review source instead")
    filt = f"loudnorm=I={target}:TP={peak}:LRA=11:linear=true:" + ":".join(
        f"{key}={measured[value]}" for key, value in keys.items())
    source_hash = before["sha256"]
    run(["ffmpeg", "-hide_banner", "-nostdin", "-n", "-i", str(path), "-map", "0:v:0?",
         "-map", "0:a:0", "-c:v", "copy", "-af", filt, "-c:a", "aac", "-b:a", "192k",
         "-ar", "48000", str(output)])
    after = inspect(output, target=target, peak=peak)
    if sha(path) != source_hash:
        raise ValueError("Input changed during processing")
    result = {"before": before, "after": after,
              "authorization_sha256": sha(authorization), "listening_review_sha256": sha(listening_review),
              "post_processing_listening": "not_checked", "user_approval": "not_checked",
              "note": "Output created, not automatically QA passed; review AAC true peak, noise and sync."}
    with sidecar.open("x", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2, allow_nan=False)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("capabilities")
    ratio = sub.add_parser("aspect")
    ratio.add_argument("width", type=int)
    ratio.add_argument("height", type=int)
    check = sub.add_parser("inspect")
    check.add_argument("input")
    check.add_argument("--expected-duration", type=float)
    check.add_argument("--target-lufs", type=float)
    check.add_argument("--peak-dbtp", type=float)
    norm = sub.add_parser("normalize")
    norm.add_argument("input")
    norm.add_argument("output")
    norm.add_argument("--target-lufs", type=float, required=True)
    norm.add_argument("--peak-dbtp", type=float, required=True)
    norm.add_argument("--authorization", required=True)
    norm.add_argument("--listening-review", required=True)
    args = parser.parse_args()
    try:
        if args.command == "capabilities":
            result = capabilities()
        elif args.command == "aspect":
            result = aspect(args.width, args.height)
        elif args.command == "inspect":
            result = inspect(args.input, args.expected_duration, args.target_lufs, args.peak_dbtp)
        else:
            result = normalize(args.input, args.output, args.target_lufs, args.peak_dbtp,
                               args.authorization, args.listening_review)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == '__main__':
    import ns_console
    ns_console.utf8()
    main()
