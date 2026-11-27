#!/usr/bin/env python3
"""Copy the issue forms, schemas and workflows from the theme into a site.

    python themes/dbaw/scripts/enable_issue_forms.py [--site-root .] [--check]

GitHub only reads issue templates from the repository they belong to, so the
forms cannot be delivered by the theme the way layouts are — they have to
exist in the site. This is the one command that puts them there, and the same
command refreshes them after the theme has moved on.

Only the files listed in presets/manifest.json are ever written. Forms and
workflows a site adds for its own sections sit outside that list and are never
touched, so re-running this is safe.

--check writes nothing and exits non-zero if anything is missing or stale,
which is how the data-checks workflow reports drift.

The version an action is pinned to (`uses: actions/checkout@v4`) is the one
thing a site is expected to change on its own, because Dependabot bumps it in
the site's copy of a workflow. It is therefore ignored when comparing, and a
refresh keeps the site's pin instead of reverting it to the preset's.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paths  # noqa: E402

MANIFEST = os.path.join(paths.PRESETS, "manifest.json")

# `uses: owner/repo[/path]@ref`, with the optional `# v4.1.0` comment that
# tools put next to a commit SHA. Local actions (`./x`) have no `@` and never
# match.
PIN = re.compile(r"(uses:[ \t]*)([^\s@]+)@(\S+)([ \t]+#[^\n]*)?")


def read(path):
    with open(path, encoding="utf-8", newline="") as handle:
        return handle.read()


def unpinned(text):
    """The text with every action's version replaced by a placeholder."""
    return PIN.sub(lambda m: m.group(1) + m.group(2) + "@*", text)


def keep_pins(text, existing):
    """`text`, but pinned to the versions `existing` already uses.

    An action that `existing` does not use keeps the version `text` names.
    """
    pins = {m.group(2): m.group(3) + (m.group(4) or "") for m in PIN.finditer(existing)}
    return PIN.sub(
        lambda m: m.group(1) + m.group(2) + "@" + pins[m.group(2)]
        if m.group(2) in pins
        else m.group(0),
        text,
    )


def planned(site):
    """(source, destination) for every file the manifest covers."""
    with open(MANIFEST, encoding="utf-8") as handle:
        manifest = json.load(handle)
    for group in manifest["groups"]:
        for name in group["files"]:
            yield (
                os.path.join(paths.PRESETS, group["source"], name),
                site.path(group["target"], name),
            )


def main():
    parser = paths.add_site_root_argument(argparse.ArgumentParser(description=__doc__))
    parser.add_argument(
        "--check",
        action="store_true",
        help="report differences instead of writing, and exit non-zero",
    )
    args = parser.parse_args()
    site = paths.Site(args.site_root)

    stale = []
    written = 0
    for source, destination in planned(site):
        if not os.path.exists(source):
            sys.exit(f"missing preset: {source}")

        wanted = read(source)
        if os.path.exists(destination):
            existing = read(destination)
            if unpinned(existing) == unpinned(wanted):
                continue
            wanted = keep_pins(wanted, existing)

        rel = os.path.relpath(destination, site.root)
        if args.check:
            stale.append(rel)
            continue

        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "w", encoding="utf-8", newline="") as handle:
            handle.write(wanted)
        print(f"wrote {rel}")
        written += 1

    if args.check:
        if stale:
            print("These files differ from the theme's presets:")
            for rel in stale:
                print("  " + rel)
            print(
                "\nRun:  python themes/dbaw/scripts/enable_issue_forms.py"
                "\nto bring them back in line."
            )
            sys.exit(1)
        print("ok — issue forms, schemas and workflows match the theme")
        return

    print(f"ok — {written} file(s) written, everything else already current")


if __name__ == "__main__":
    main()
