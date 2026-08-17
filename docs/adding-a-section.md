# Adding a section

Everything here happens in your own site. The theme is not forked, edited or
touched.

## The minimum

Two files. Say you want a Grants section.

**1. `data/grants.json`** — an array of flat records:

```json
[
  {
    "title": "Adaptive methods for thin-shell analysis",
    "funder": "National Science Foundation",
    "description": "Four-year personal fellowship.",
    "year": "2025",
    "url": "https://example.org/fellowship",
    "featured": true
  }
]
```

**2. an entry in `data/sections.json`** describing how to render it:

```json
{
  "id": "grants",
  "style": "generic",
  "label": "Grants & Funding",
  "cvLabel": "Grants & Funding",
  "weight": 55,
  "titleField": "title",
  "subtitleField": "funder",
  "bodyField": "description",
  "dateField": "year",
  "linkField": "url"
}
```

That is it. The section appears on the homepage, in the navigation, and in the
generated CV. `weight` places it — the built-in sections are spaced ten apart in
declaration order, so `55` puts it between the fifth and sixth.

`style: "generic"` selects the field-driven renderer. Without it the theme would
look for a `grants` preset, not find one, and fall back to the generic renderer
anyway — but saying so is clearer.

## The optional extras

Each of these is independent; take the ones you want.

| You also want | Add |
| --- | --- |
| A page of its own at `/grants/`, and a linked heading | `content/grants/_index.md` with a `title` |
| CI validation of the data | `.github/schemas/grants.schema.json` |
| Editor autocomplete | an entry in `.vscode/settings.json` pointing at that schema |
| To add entries by filling in a form | `.github/ISSUE_TEMPLATE/grant.yml` + a `grants:` block in `.github/data-entry/sections.yml` |
| Markup the generic renderer cannot produce | `layouts/partials/sections/grants.html` in **your** repository |

The last one is worth understanding: the theme resolves renderers with
`templates.Exists`, which searches your site's layouts as well as the theme's.
Dropping that file in takes over rendering with no configuration change, and
deleting it hands rendering back. You can start generic and specialise later.

Its context is `.section` (the registry entry, with defaults filled in) and
`.pages` (the records). Copy any of the theme's
`layouts/partials/sections/*.html` as a starting point.

## Registry keys

Only `id` is required; everything else defaults.

| Key | Default | Meaning |
| --- | --- | --- |
| `id` | — | Anchor, and the default for `data`, `style` and the label lookup |
| `data` | `id` | Data file, without `.json` |
| `style` | `id` | Renderer to look for before falling back to generic |
| `label` | i18n lookup on `id`, else a humanised `id` | Heading on the site |
| `cvLabel` | `label` | Heading in the CV, usually longer |
| `enable` | `true` | Set false to hide without deleting |
| `inCV` | `true` | Set false to leave out of the PDF |
| `featuredOnly` | `true` | Homepage shows only `"featured": true` records |
| `homepageLimit` | `0` | Cap homepage records; 0 is no cap |
| `weight` | declaration order × 10 | Ordering |
| `sortField` / `sortReverse` | unsorted / `true` | Sort records before rendering |
| `groupField` | — | Emit a subheading per distinct value |
| `titleField` … `detailsField` | `title`, `subtitle`, `description`, `date`, `url`, `details` | Field mapping for the generic renderer |

## Why the registry lives in `data/`

Because the CV reads it. `latex/autoCV.tex` parses JSON at compile time and has
no TOML parser, and `compile_CV.sh` runs before Hugo, so a registry in
`hugo.toml` could not be shared with it. Keeping it in `data/sections.json`
means the website and the PDF cannot disagree about which sections exist.

## A caveat worth knowing

The built-in presets — publications, experience, awards, teaching, supervision,
conferences — dispatch on an enum field (`entry-type`, `type`, `level`,
`invited`) with no fallback branch. A typo there drops the record from the site
*and* the CV while both still build cleanly. That is what the JSON Schemas are
for; run `python themes/dbaw/scripts/validate_data.py` and let CI run it too.

The generic renderer has no such trap: unmapped fields are simply not shown.
