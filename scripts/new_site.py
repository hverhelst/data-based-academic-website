#!/usr/bin/env python3
"""Scaffold a new site that uses this theme.

    python scripts/new_site.py --target ../my-website --name "Ada Lovelace"

Writes a hugo.toml, a bio page, an empty data file per built-in section, and a
data/sections.json registry. It does not add the submodule or run git — it
prints the two commands to run next, so nothing happens to your repository
that you did not type.

Existing files are never overwritten; the run reports what it skipped.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paths  # noqa: E402

SECTIONS = [
    ("news", "News", None),
    ("education", "Education", "Education"),
    ("experience", "Experience", "Experience"),
    ("awards", "Awards, Honours and Memberships", "Awards & Memberships"),
    ("publications", "Publications", "Publications"),
    ("conferences", "Conferences", "Conference and seminar presentations"),
    ("software", "Software", "Software contributions"),
    ("teaching", "Teaching", "Teaching experience"),
    ("supervision", "Supervision & Committee work", "Supervision & Committee work"),
]

CONFIG = '''theme = "dbaw"
baseURL = "{baseurl}"
locale = "en"
title = "{name}"
dateFormat = "January 2, 2006"
disableKinds = ["taxonomy", "term"]

[params]
firstName = "{first}"
lastName = "{last}"
address = "Your city, Your country"
email = "you@example.edu"
profileImage = "img/profile.jpg"
CVlink = "doc/CV.pdf"
showSocializations = true

# Sections are declared in data/sections.json, not here — the LaTeX CV reads
# that same file, which is what keeps the site and the PDF in step.

[[params.handles]]
name = "GitHub"
link = "https://github.com/yourname"
icon = "github"

[[params.handles]]
name = "ORCID"
link = "https://orcid.org/0000-0000-0000-0000"
icon = "orcid"

[params.meta]
description = "{name}"
author = "{name}"
favicon = true

[markup.goldmark.renderer]
unsafe = true
'''

BIO = '''---
title: "Home"
sitemap:
  priority: 1.0
---
Hi, I'm {name}. Replace this paragraph with a short bio — it is ordinary
markdown, and the only prose on the homepage. Everything below it comes from
`data/`.
'''


def write(path, text, skipped):
    if os.path.exists(path):
        skipped.append(path)
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="directory for the new site")
    parser.add_argument("--name", default="Your Name")
    parser.add_argument("--baseurl", default="https://example.org/")
    args = parser.parse_args()

    root = os.path.abspath(args.target)
    first, _, last = args.name.partition(" ")
    skipped = []

    write(
        os.path.join(root, "hugo.toml"),
        CONFIG.format(
            name=args.name, first=first, last=last or first, baseurl=args.baseurl
        ),
        skipped,
    )
    write(os.path.join(root, "content", "_index.md"), BIO.format(name=args.name), skipped)

    registry = []
    for section, label, cv_label in SECTIONS:
        entry = {"id": section}
        if cv_label is None:
            entry["inCV"] = False
        else:
            entry["cvLabel"] = cv_label
        registry.append(entry)
        write(os.path.join(root, "data", section + ".json"), "[]\n", skipped)
        write(
            os.path.join(root, "content", section, "_index.md"),
            '---\ntitle: "%s"\nweight: 10\nsitemap:\n  priority: 0.6\n---\n' % label,
            skipped,
        )

    write(
        os.path.join(root, "data", "sections.json"),
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        skipped,
    )
    write(
        os.path.join(root, "data", "mydata.json"),
        json.dumps(
            {
                "name": args.name,
                "citationName": args.name,
                "university": "Your University",
                "department": "Your Department",
                "email": "you@example.edu",
                "website": args.baseurl,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        skipped,
    )
    write(
        os.path.join(root, ".gitignore"),
        "public/\nbuild/\n.hugo_build.lock\n__pycache__/\nstatic/doc/CV.pdf\n",
        skipped,
    )

    for path in skipped:
        print("skipped (exists): " + os.path.relpath(path, root))

    print(
        "\nScaffolded {0}\n\nNext:\n"
        "  cd {0}\n"
        "  git init\n"
        "  git submodule add https://github.com/hverhelst/data-based-academic-website themes/dbaw\n"
        "  hugo server\n\n"
        "Optional, to add entries by filling in an issue form:\n"
        "  python themes/dbaw/scripts/enable_issue_forms.py\n".format(root)
    )


if __name__ == "__main__":
    main()
