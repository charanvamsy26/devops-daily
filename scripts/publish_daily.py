#!/usr/bin/env python3
"""Publish the next queued TIL entry as today's entry, update the index, commit, push.

Run daily by .github/workflows/daily.yml inside GitHub Actions (so it does not
depend on any local machine being on). Idempotent: if today's entry already
exists, it does nothing and exits 0.

Queue files live in queue/ named NN-slug.md and contain a full entry whose H1
uses the literal placeholder {{DATE}}, e.g. "# {{DATE}} — Topic Title". The
lowest-numbered queue file is published next, then removed.
"""
from __future__ import annotations

import datetime as dt
import glob
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(REPO, "entries")
QUEUE = os.path.join(REPO, "queue")
README = os.path.join(REPO, "README.md")
MARKER = "<!-- NEXT-ENTRY -->"


def run(*args: str) -> None:
    subprocess.run(args, cwd=REPO, check=True)


def main() -> int:
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    target = os.path.join(ENTRIES, f"{today}.md")
    if os.path.exists(target):
        print(f"entry for {today} already exists; nothing to do")
        return 0

    queued = sorted(glob.glob(os.path.join(QUEUE, "*.md")))
    if not queued:
        print("::warning::TIL queue is empty — nothing to publish. Please refill queue/.")
        return 0

    src = queued[0]
    with open(src, encoding="utf-8") as fh:
        dated = fh.read().replace("{{DATE}}", today)

    topic_m = re.search(r"^#\s*.*?—\s*(.+?)\s*$", dated, re.MULTILINE)
    topic = topic_m.group(1).strip() if topic_m else "Untitled"
    area_m = re.search(r"\*\*Area:\*\*\s*(.+?)\s*·", dated)
    area = area_m.group(1).strip() if area_m else ""

    os.makedirs(ENTRIES, exist_ok=True)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(dated)

    with open(README, encoding="utf-8") as fh:
        readme = fh.read()
    row = f"| [{today}](entries/{today}.md) | {topic} | {area} |\n"
    if MARKER in readme:
        readme = readme.replace(MARKER, row + MARKER)
    else:
        print("::warning::index marker not found; README index not updated")
    with open(README, "w", encoding="utf-8") as fh:
        fh.write(readme)

    os.remove(src)

    remaining = len(queued) - 1
    if remaining <= 5:
        print(f"::warning::only {remaining} queued entries left — refill queue/ soon")

    run("git", "add", "-A")
    run("git", "commit", "-m", f"docs: {today} — {topic}")
    run("git", "push")
    print(f"published {today}: {topic} ({area}); {remaining} left in queue")
    return 0


if __name__ == "__main__":
    sys.exit(main())
