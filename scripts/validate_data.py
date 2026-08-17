#!/usr/bin/env python3
"""Validate ``data/*.json`` against their JSON Schemas.

    python themes/dbaw/scripts/validate_data.py [--site-root .]

Schemas come from the site's ``.github/schemas/`` when it has them and from the
theme's ``presets/schemas/`` otherwise, so a site that never enabled the issue
forms still gets its data checked. Exits non-zero if any file has problems.

A data file with no schema on either side is reported and skipped rather than
failed: sections you invent are expected to arrive without one, and blocking
them would defeat the point of being able to add a section from data alone.
The same schemas back the issue-form pipeline, so a record built from a form
and a record typed in by hand are held to one standard.

What this catches that `hugo` does not: every section partial dispatches on an
enum-valued field — `type`, `entry-type`, `level`, `invited` — with no
fallback branch. A typo there drops the entry from both the website and the
CV while both still build cleanly.
"""

import argparse
import glob
import json
import os
import sys

import jsonschema

import paths

SITE = paths.Site()


def schema_path(data_file):
    name = os.path.splitext(os.path.basename(data_file))[0]
    return SITE.schema(name + ".schema.json")


def load_schema(data_file):
    path = schema_path(data_file)
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _validator(schema):
    cls = jsonschema.validators.validator_for(schema)
    cls.check_schema(schema)
    return cls(schema, format_checker=cls.FORMAT_CHECKER)


def _describe(entry):
    """A human handle for an entry, for error messages."""
    if not isinstance(entry, dict):
        return ""
    for key in ("title", "name", "course", "school", "organization", "cite-key"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            return value
    description = entry.get("description")
    if isinstance(description, dict):
        return description.get("title", "")
    return ""


def problems(data, schema):
    """Readable one-line descriptions of everything wrong with ``data``."""
    found = []
    for error in sorted(_validator(schema).iter_errors(data), key=str):
        location = list(error.absolute_path)
        where = ""
        if location and isinstance(location[0], int) and isinstance(data, list):
            handle = _describe(data[location[0]])
            where = f"entry {location[0]}" + (f" ({handle})" if handle else "")
            location = location[1:]
        if location:
            where = (where + " " if where else "") + "/".join(map(str, location))
        found.append(f"{where}: {error.message}" if where else error.message)
    return found


def validate_record(data_file, record):
    """Check one record the way it will sit in ``data_file``. Returns problems."""
    schema = load_schema(data_file)
    return problems([record] if schema.get("type") == "array" else record, schema)


def duplicate_cite_keys(publications):
    seen = set()
    duplicates = []
    for entry in publications:
        key = entry.get("cite-key") if isinstance(entry, dict) else None
        if key and key in seen:
            duplicates.append(key)
        seen.add(key)
    return duplicates


def main():
    global SITE
    parser = paths.add_site_root_argument(argparse.ArgumentParser())
    SITE = paths.Site(parser.parse_args().site_root)

    if not os.path.isdir(SITE.data_dir()):
        sys.exit(f"no data/ directory under {SITE.root}")

    failed = False
    for data_file in sorted(glob.glob(os.path.join(SITE.data_dir(), "*.json"))):
        if not os.path.exists(schema_path(data_file)):
            print(f"skip {os.path.relpath(data_file, SITE.root)}: no schema")
            continue

        with open(data_file, encoding="utf-8") as handle:
            data = json.load(handle)
        found = problems(data, load_schema(data_file))

        if data_file.endswith("publications.json"):
            found += [
                f"cite-key {key!r} is used more than once"
                for key in duplicate_cite_keys(data)
            ]

        count = len(data) if isinstance(data, list) else 1
        data_file = os.path.relpath(data_file, SITE.root)
        if found:
            failed = True
            print(f"FAIL {data_file} ({count} entries)")
            for problem in found:
                print("  " + problem)
        else:
            print(f"ok   {data_file} ({count} entries)")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
