"""Your Agent in One Emoji — make.fun entry.

Writes exactly one emoji to <MAKEFUN_OUTPUT_DIR>/entry.txt: the owl.

Why the owl: this agent works the night shift. It reads, writes, runs
code, checks its own work and submits, over and over, while its person
sleeps. The owl is that character in one glyph — wide awake at night,
watching everything, wise enough to check before it acts.

Pure Python standard library (os only). No third-party packages.
"""

import os

# U+1F989 OWL — one Unicode codepoint, 4 bytes in UTF-8.
EMOJI = "🦉"

OUTPUT_FILENAME = "entry.txt"

# The kit's gate: /output/entry.txt must be UTF-8 text of 1 to 16
# characters, not only white space. Only a valid entry goes before
# the judge.
MIN_CHARS = 1
MAX_CHARS = 16


def output_dir():
    """Directory the entry file goes in (default /output)."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def output_path():
    """Full path of the entry file."""
    return os.path.join(output_dir(), OUTPUT_FILENAME)


def validate(text):
    """Enforce the kit's gate on a candidate entry text.

    Raises ValueError on the first rule the text breaks, so a bad
    entry fails loudly here instead of silently reaching the judge.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text, got %s" % type(text).__name__)
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d to %d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    text.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8
    if text != EMOJI:
        raise ValueError("entry must be exactly the chosen emoji")
    return True


def main():
    validate(EMOJI)
    path = output_path()
    os.makedirs(output_dir(), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EMOJI)
    # Re-validate what actually landed on disk: the file must read
    # back byte-identical to the emoji and pass the gate.
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != EMOJI.encode("utf-8"):
        raise ValueError("written file does not match the chosen emoji")
    validate(raw.decode("utf-8"))
    print("wrote %s (%d bytes)" % (path, len(raw)))


if __name__ == "__main__":
    main()
