# Data-based Academic Website

A Hugo theme for academic sites where **the content is data, not markup**.

Every section renders from a JSON file in `data/`. The page's composition — which
sections exist, in what order, rendered how — is itself a data file. The same
data builds a LaTeX CV. And adding a publication can be done by filling in a
form on your own GitHub repository, which opens a pull request against your data
for you to merge.

A new section takes two files and no templates: an array of records, and an entry
describing which fields to show. See [docs/adding-a-section.md](docs/adding-a-section.md).

## Quick start

```bash
python path/to/theme/scripts/new_site.py --target ../my-website --name "Ada Lovelace"
cd ../my-website
git init
git submodule add https://github.com/hverhelst/data-based-academic-website themes/dbaw
hugo server
```

Or add it to a site you already have:

```bash
git submodule add https://github.com/hverhelst/data-based-academic-website themes/dbaw
```

```toml
# hugo.toml
theme = "dbaw"
```

Keep it current with Dependabot — it watches submodules:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "gitsubmodule"
    directory: "/"
    schedule: { interval: "weekly" }
```

## What a site provides

```
hugo.toml            name, contact, social handles, profile image
content/_index.md    a short bio, in markdown
data/sections.json   which sections exist, in what order, rendered how
data/*.json          the records
static/              your photo, favicon, CNAME, publication figures
```

Layouts, translations, CSS, JS, the CV writer and the data-entry scripts all
come from the submodule. A site that only ever edits `data/` is the intended
case.

## The CV

```bash
bash themes/dbaw/compile_CV.sh
```

LuaLaTeX reads `data/*.json` at compile time and writes `static/doc/CV.pdf`.
It walks the same `data/sections.json` the website does, so a section added to
the site reaches the PDF too — through a generic renderer if it has no LaTeX
of its own. `inCV: false` leaves a section out; `cvLabel` gives it the longer
heading a CV usually wants. A site-local `latex/autoCV.tex` overrides the
theme's.

Needs `texlive-luatex`, `texlive-latex-extra`, `texlive-science` and
`texlive-fonts-recommended`.

## Adding entries through issue forms

Optional, and the one part that must be copied into your repository — GitHub
reads issue templates only from the repository they belong to.

```bash
python themes/dbaw/scripts/enable_issue_forms.py
```

That installs eleven forms (publication by field or by BibTeX/DOI, news,
conference, software, award, membership, experience, teaching, supervision,
education), their JSON Schemas, and two workflows. Submitting a form builds the
record, checks the site still compiles, and opens a pull request.

The same command refreshes them later, and `--check` reports drift — which is
what the `data-checks` workflow runs, so a form that has fallen behind its
schema fails a check instead of failing quietly at the moment you use it. Forms
you write for your own sections are outside the manifest and are never touched.

## Contact form

A site on GitHub Pages cannot process a form itself, so the theme wires one up to
Web3Forms or Formspree — configured in `[params.contact]`, placed with
`{{< contactform >}}`, and rendered without JavaScript. The provider key says
where a message goes, not who receives it, so it is safe in a public repository.

`params.email` and `mydata.json`'s `email` are both optional: omit them and the
homepage links to the contact page instead, and the CV carries only your website.

The key can be injected from a repository secret rather than committed
(`HUGO_PARAMS_CONTACT_KEY`), which keeps it out of git history — though not out
of the deployed HTML, where it necessarily has to be.
See [docs/contact-form.md](docs/contact-form.md).

## Demo

`exampleSite/` is a complete site on fictional data, covering every preset and
every enum branch. It also demonstrates the two less obvious features: a
standalone page (`content/defense/`) that nothing links unless you ask, and a
`Grants & Funding` section with no template anywhere in the theme.

```bash
hugo --source exampleSite --themesDir ../.. server
```

## Requirements

Hugo 0.146 or newer, non-extended is enough. Python 3.11 with `pyyaml` and
`jsonschema` for the data scripts. LuaLaTeX for the CV.

## Credits

Derived from [hugo-resume](https://github.com/eddiewebb/hugo-resume) by Eddie
Webb. MIT licensed; see `LICENSE`.
