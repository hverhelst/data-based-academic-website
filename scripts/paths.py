#!/usr/bin/env python3
"""Where the scripts look for the site's files, and for their own.

These scripts live in the theme and run against a site that has them checked
out as a submodule, so "the repository root" is no longer the directory the
script sits in. Everything site-owned is resolved from a site root (the
current directory by default, overridable with --site-root); everything
theme-owned is resolved from this file's location.

Schemas are the one thing that can come from either side: a site may vendor
its own copy under .github/schemas/ — and must, for sections it invented — but
a site that never enabled the issue forms still gets its data validated
against the presets shipped here.
"""

import os

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.dirname(SCRIPTS)
PRESETS = os.path.join(THEME, "presets")
PRESET_SCHEMAS = os.path.join(PRESETS, "schemas")
PRESET_FORMS = os.path.join(PRESETS, "issue-forms")


class Site:
    """Paths inside the site being built, as opposed to inside the theme."""

    def __init__(self, root="."):
        self.root = os.path.abspath(root or ".")

    def path(self, *parts):
        return os.path.join(self.root, *parts)

    def data(self, name):
        """A data file, given either a bare name or a "data/x.json" path."""
        if os.path.isabs(name):
            return name
        if name.startswith("data" + os.sep) or name.startswith("data/"):
            return self.path(name)
        return self.path("data", name)

    def data_dir(self):
        return self.path("data")

    def media_dir(self):
        return self.path("static", "media")

    def forms_dir(self):
        """The site's issue forms, falling back to the theme's presets.

        Only the site's copy can drive a real issue — GitHub reads templates
        from the repository itself — but the presets let the self-test run
        against a site that has not enabled the forms.
        """
        local = self.path(".github", "ISSUE_TEMPLATE")
        return local if os.path.isdir(local) else PRESET_FORMS

    def schema(self, name):
        """A schema by file name, site copy winning over the theme's preset."""
        local = self.path(".github", "schemas", name)
        return local if os.path.exists(local) else os.path.join(PRESET_SCHEMAS, name)


def add_site_root_argument(parser):
    """Register the flag every entry point shares."""
    parser.add_argument(
        "--site-root",
        default=os.environ.get("SITE_ROOT", "."),
        help="root of the website repository (default: current directory)",
    )
    return parser
