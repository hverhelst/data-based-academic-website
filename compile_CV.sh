#!/bin/bash
# Builds the CV PDF from latex/autoCV.tex + the site's data/*.json.
#
# The Lua code inside autoCV.tex opens data/*.json with CWD-relative paths, so
# this MUST run with the *site* as the working directory — which is no longer
# the directory the script lives in, now that the script ships with the theme.
# Set SITE_ROOT to build a site other than the current directory.
#
# A site that wants its own layout can keep a latex/autoCV.tex of its own; it
# wins over the theme's copy.
set -euo pipefail

THEMEDIR="$(cd "$(dirname "$0")" && pwd)"
cd "${SITE_ROOT:-$PWD}"

TEXFILE="$THEMEDIR/latex/autoCV.tex"
if [ -f "latex/autoCV.tex" ]; then
    TEXFILE="$PWD/latex/autoCV.tex"
fi

BUILDDIR=build/CV
mkdir -p "$BUILDDIR" static/doc

# Two passes: lastpage + hyperref need a second run for \pageref{LastPage}.
for pass in 1 2; do
    lualatex --interaction=nonstopmode --halt-on-error \
             --output-directory="$BUILDDIR" "$TEXFILE"
done

cp "$BUILDDIR/autoCV.pdf" static/doc/CV.pdf
echo "CV written to $PWD/static/doc/CV.pdf (from $TEXFILE)"
