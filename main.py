#!/usr/bin/env python3
"""Write one line about office life to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The line is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition brief: one line, 1 to 200 characters, not only white space.
"""

import os
import sys
from pathlib import Path

# Make sibling imports resolve even when the grader runs with -P:
# the script's own directory goes first on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))

LINE = "We got standing desks so we could stand more, and now we all sit on taller chairs."

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path(argv, environ) -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(argv) > 1:
        return Path(argv[1])
    env_path = environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the brief: one line, 1 to 200 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"line is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("line is only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    return chars


def write_entry(path: Path, text: str) -> None:
    """Write the line to path, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run(argv, environ) -> int:
    """Validate the line, resolve the output path, write it, report back.

    Kept separate from main() so the work takes explicit inputs instead of
    reading sys.argv and os.environ directly; main() is a thin wrapper.
    """
    try:
        chars = validate(LINE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path(argv, environ)
    write_entry(path, LINE)
    print(f"wrote {chars} characters to {path}")
    return 0


def main() -> int:
    return run(sys.argv, os.environ)


if __name__ == "__main__":
    raise SystemExit(main())
