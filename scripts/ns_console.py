"""Console encoding for CLI entry points; Windows consoles and pipes may default to cp1252."""
import sys


def utf8():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='backslashreplace')
        except (AttributeError, ValueError):
            pass
