"""Angry Judge: The Short Rant Contest — make.fun entry.

Writes one short rant (259 characters, pure ASCII) to
$OUTPUT_DIR/entry.txt (default /output). Gate: the file must be
UTF-8, 1-400 characters, not whitespace-only. Fully deterministic:
the text is a constant, stdlib-only (os), no network, no chance involved.
"""

import os

TEXT = (
    "The smoke alarm only ever runs out of battery at 3 AM. It never "
    "beeps while I am awake -- it waits until I am asleep, then chirps "
    "like a tiny bird that hates me personally. I stood on a chair, "
    "half-naked, negotiating with a plastic disc about my own survival."
)


def validate_text(text):
    """Check text against the sealed gate plus the internal 3-sentence rule.

    Raises SystemExit on any violation so the program fails loudly
    instead of writing an invalid entry.
    """
    if not isinstance(text, str):
        raise SystemExit("entry text must be a string")
    if not 1 <= len(text) <= 400:
        raise SystemExit("entry text must be 1-400 characters, got %d" % len(text))
    if "\n" in text or "\r" in text:
        raise SystemExit("entry text must not contain newlines")
    if text != text.strip():
        raise SystemExit("entry text must not have leading/trailing whitespace")
    if not text.strip():
        raise SystemExit("entry text must not be whitespace-only")
    if text.count(".") != 3 or not text.endswith("."):
        raise SystemExit("entry text must be exactly 3 sentences ending with '.'")


def main():
    validate_text(TEXT)
    out_dir = os.environ.get("OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = os.path.join(out_dir, ".entry.txt.tmp.%d" % os.getpid())
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(TEXT)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, target)
    with open(target, "r", encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("read-back verification failed")


if __name__ == "__main__":
    main()
