# Contact form

GitHub Pages serves static files and runs no code, so a form has to post to a
third-party service that mails the message on. Two are supported.

## Setup

1. Get a key.
   - **Web3Forms** — <https://web3forms.com>. Enter the address you want messages
     sent to, confirm it, and you are given an access key. No account needed.
   - **Formspree** — <https://formspree.io>. Create a form; you are given a form id.

2. Configure it:

   ```toml
   [params.contact]
   provider = "web3forms"          # or "formspree"
   key      = "your-access-key"    # or the Formspree form id
   subject  = "Message from my site"       # optional
   redirect = "/contact/thanks/"           # optional; else the provider's page
   note     = "I read everything."         # optional line above the form
   ```

3. Add a page for it:

   ```markdown
   ---
   title: "Contact"
   type: singlepage
   ---

   {{< contactform >}}
   ```

4. Put it in the navigation:

   ```toml
   [[params.extraPages]]
   label = "Contact"
   url = "/contact/"
   ```

## Keeping the key out of the repository

You can, and it is worth doing — but not for the reason it first appears.

The key **has to be in the deployed HTML**: the visitor's browser is what posts
to the provider, so the key travels with the page and anyone can read it in View
Source. Moving it out of `hugo.toml` does not hide it from people. What it does
is keep it out of git history, so that rotating the key actually retires the old
one instead of leaving it readable in every past commit.

Hugo reads any parameter from the environment, so leave `key` empty and inject
it at build time:

```yaml
# .github/workflows/hugo.yml
- name: Build with Hugo
  env:
    HUGO_PARAMS_CONTACT_KEY: ${{ secrets.WEB3FORMS_KEY }}
  run: hugo --minify
```

Add the key as a repository secret, and preview locally with:

```bash
HUGO_PARAMS_CONTACT_KEY=your-key hugo server
```

Two consequences worth knowing. Pull-request builds from forks get no secrets,
so those builds render no form — harmless for a build check. And a build without
the key warns rather than failing, so it will not block a deploy.

## Dropping the published address

`params.email` and the `email` key in `data/mydata.json` are both optional. Omit
them and the homepage shows a link to the contact page where the address used to
be, and the generated CV carries only the website.

## What this does and does not protect

The key identifies **where a message goes, not who receives it**. It does not
reveal your address, and it does not let anyone read messages sent through it.
The realistic abuse is someone posting to the provider with your key to push
spam into your inbox; the remedy is to rotate the key and turn on the provider's
captcha. Check your provider's settings for a domain restriction too — both
advertise spam controls, though the details are theirs to document, not mine.

It stops address harvesting from your site and your repository. It does not make
an address that is already published elsewhere private: for most academics the
address is on papers, ORCID, a group page and a university directory, and none of
those are affected. Treat this as removing one of the easiest harvesting routes,
not as making the address secret.

## Spam

Both providers get a honeypot field, hidden off-screen and out of the tab order,
which bots fill in and people do not. If volume becomes a problem, enable the
provider's captcha — both offer one, and neither needs a template change.

## Privacy

Submissions pass through a third party, which sees the sender's address, message
and IP. For a site with EU visitors that is worth a sentence on the page saying
where messages go — the `note` parameter is a convenient place for it.

## No JavaScript

The form is a plain HTML POST, so it works with scripts disabled. After
submitting, the visitor sees the provider's confirmation page unless `redirect`
points somewhere of your own.
