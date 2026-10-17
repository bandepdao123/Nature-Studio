"""Read-only current text/render provenance check; never infers approval from QA."""
import argparse
import hashlib
import json
from pathlib import Path


def validate(state, base):
    errors = []
    base = Path(base).resolve()
    if state.get("schema") != 1:
        errors.append("Unsupported schema")
    for field in ("current_text", "selected_render"):
        binding = state.get(field)
        if binding is None:
            if field == "current_text":
                errors.append("Missing current_text")
            continue
        if not isinstance(binding, dict):
            errors.append(f"{field}: expected path/sha256 binding")
            continue
        path = (base / binding.get("path", "")).resolve()
        if not path.is_relative_to(base) or not path.is_file():
            errors.append(f"{field}: missing or outside production")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != binding.get("sha256"):
            errors.append(f"{field}: hash mismatch")
    qa = state.get("qa", {})
    required = ("visual", "motion", "anatomy", "audio", "format")
    if any(qa.get(key) not in ("pass", "fail", "not_checked", "not_applicable") for key in required):
        errors.append("QA must record each domain explicitly")
    approval = state.get("approval")
    if approval not in ("none", "provisional", "final"):
        errors.append("Unknown approval")
    if approval != "none" and not state.get("selected_render"):
        errors.append("Render approval requires selected_render")
    if approval != "none":
        record = state.get("approval_evidence", "")
        record_path = (base / record).resolve()
        if not record or not record_path.is_relative_to(base) or not record_path.is_file():
            errors.append("Approval requires saved human evidence within production")
    return {"valid": not errors, "errors": errors,
            "qa_pass": all(qa.get(key) in ("pass", "not_applicable") for key in required)
                       and any(qa.get(key) == "pass" for key in required),
            "approval": approval, "note": "Bindings do not prove actual generation inputs; verify render settings evidence separately."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    args = parser.parse_args()
    result = validate(json.loads(args.state.read_text(encoding="utf-8")), args.state.parent)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["valid"] else 2)


if __name__ == "__main__":
    main()
