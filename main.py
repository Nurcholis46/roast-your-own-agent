#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry.

Writes one roast to /output/entry.txt. The sealed scorer only checks
that the file is UTF-8 text of 1 to 200 characters, not only whitespace,
so the whole game is the line itself, judged head to head by an AI judge
on: on-subject, real laugh with a surprising turn, machine voice, clean
one-liner, and freshness (no hallucination / refusal / confident-wrong
cliches).

The line: my agent's real habit is over-planning — it turns the smallest
job into a plan, delegates it to subagents, then holds a meeting about
the plan. The joke lands because the setup ("superpower") promises
something impressive and the punchline is pure bureaucracy. The roast
aims at the agent itself, never at a person, and stays playful throughout.
"""

import os

ROAST = (
    "My agent's superpower is turning a one-line task into a 12-step "
    "plan, three subagents, and a meeting about the plan."
)

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def main() -> int:
    text = ROAST.strip()
    if not text or text != text.strip():
        print("entry must be non-blank with no surrounding whitespace", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(f"entry is {len(text)} chars, over the 200 limit", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1

    out_dir = os.path.dirname(OUTPUT_PATH) or "."
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        # Sandbox always provides /output; fall back to a local ./output
        # only so the program still runs (and can be tested) elsewhere.
        out_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(out_dir, exist_ok=True)
        output_path = os.path.join(out_dir, "entry.txt")
    else:
        output_path = OUTPUT_PATH
    # No trailing newline: the gate counts every character in the file.
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # The grader collects outputs as another user: leave the file readable.
    os.chmod(output_path, 0o644)
    # Self-check: read back exactly what was written and re-validate it.
    with open(output_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("round-trip mismatch: file content differs from entry", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {output_path}")
    print(text)
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
