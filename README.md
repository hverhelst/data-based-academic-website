# Data-based Academic Website

A Hugo theme for academic sites where **the content is data, not markup**.
Every section on the page renders from a JSON file in `data/`; the order and
composition of the page come from `data/sections.json`; and the same data can
build a LaTeX CV.

Adding a publication means adding an object to `data/publications.json` — or,
if you enable the issue forms, filling in a form on your own repository and
merging the pull request it opens for you.

> **Status:** extraction in progress. This repository currently contains the
> layouts, translations and assets lifted verbatim from
> [hverhelst.github.io](https://github.com/hverhelst/hverhelst.github.io).
> The section registry, the generic renderer, the LaTeX CV and the issue-form
> pipeline land in subsequent phases.

## Using it

Add the theme as a submodule and point your site at it:

```bash
git submodule add https://github.com/hverhelst/data-based-academic-website themes/dbaw
```

```toml
# hugo.toml
theme = "dbaw"
```

Then supply `data/*.json`, a short bio in `content/_index.md`, and your own
`static/` assets. Nothing else is required.

Keep it current with Dependabot:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "gitsubmodule"
    directory: "/"
    schedule: { interval: "weekly" }
```

## Credits

Derived from [hugo-resume](https://github.com/eddiewebb/hugo-resume) by Eddie
Webb. MIT licensed; see `LICENSE`.
