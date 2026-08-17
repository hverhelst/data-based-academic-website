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
"""

import argparse
import filecmp
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paths  # noqa: E402

MANIFEST = os.path.join(paths.PRESETS, "manifest.json")


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

        current = os.path.exists(destination) and filecmp.cmp(
            source, destination, shallow=False
        )
        if current:
            continue

        rel = os.path.relpath(destination, site.root)
        if args.check:
            stale.append(rel)
            continue

        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copyfile(source, destination)
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
