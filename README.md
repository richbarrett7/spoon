# Spoon Cereals

## How to build

To make it easier to manage common components without an overbearing framework, I have made a very simple build tool `build.py`.

Simply run this python script on the command line and it'll take html files in src/ and put copy them to public/ but replacing some placeholders first ...

{{ abc.include.html }} with be replaced with content of `src/abc.include.html`

{{ cachebust }} will be replaced with a hash (generated using timestamp), useful for CSS etc.

### Future

Arguably if deploying to Cloudflare pages, you could omit the public/ html files from the repository and have them built on deploy.  I've not gone this far for now.