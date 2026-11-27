---
title: "Home"
sitemap:
  priority: 1.0
---
 **This is the demo site for the [Data-based Academic Website](https://github.com/hverhelst/data-based-academic-website) theme, not a personal homepage.** The real one is at [hugoverhelst.nl](https://hugoverhelst.nl). The name and the entries below are a trimmed subset of that site's data, so the demo shows the layout with realistic content instead of filler.

 Everything under this paragraph is rendered from JSON files in `data/`. The order of the sections, and how each one is rendered, comes from `data/sections.json` — the same file the LaTeX CV reads, which is what keeps the website and the PDF from drifting apart.

 The **Example section** near the bottom is the interesting one: the theme contains no template for it, in Go or in LaTeX. It appears on this page, on a page of its own, and in the [CV](doc/CV.pdf) because `data/sections.json` says it exists and names which fields to show.
