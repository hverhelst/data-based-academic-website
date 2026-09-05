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

## Dropping the published address

`params.email` and the `email` key in `data/mydata.json` are both optional. Omit
them and the homepage shows a link to the contact page where the address used to
be, and the generated CV carries only the website.

## What this does and does not protect

The key in the page identifies **where a message goes, not who receives it**, so
it is safe in a public repository — that is the whole point of the arrangement.

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
