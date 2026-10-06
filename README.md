# Minimal Theme

[Demo the Theme](http://orderedlist.github.com/minimal/)

This is the raw HTML and styles that are used for the *minimal* theme on [GitHub Pages](http://pages.github.com/).

Syntax highlighting is provided on GitHub Pages by [Pygments](http://pygments.org).

# License

This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).




### Blog search metadata

After editing or adding a blog post, run `python3 scripts/build-blog-seo.py`
(requires `beautifulsoup4`). It refreshes JSON-LD, social previews, the sitemap,
and RSS from the HTML pages; legacy redirect pages are excluded. New collection
pages need an entry in `COLLECTIONS`. Article descriptions currently cover the
three translations of the first post. Update that configuration for new articles.

Submit `https://seominseok0429.github.io/sitemap.xml` in Google Search Console
and Bing Webmaster Tools after verifying site ownership. Publishing the sitemap
does not itself submit it to those accounts or guarantee indexing/ranking.

### IndexNow notifications

The root `954cf3b72217415380cf3ef657fa4ead.txt` file verifies site ownership
for [IndexNow](https://www.indexnow.org/documentation). Keep it deployed.
The submission script uses only Python's standard library and selects canonical
URLs from `sitemap.xml`, excluding legacy redirects and asset files.

After GitHub Pages finishes deploying new or meaningfully updated content,
preview the affected URLs and then submit them:

```sh
python3 scripts/submit-indexnow.py https://seominseok0429.github.io/blog/
python3 scripts/submit-indexnow.py --submit https://seominseok0429.github.io/blog/
```

Pass multiple URLs when needed. For initial setup, `--all` previews all sitemap
URLs; `--all --submit` verifies the live key and submits that batch. Avoid
repeatedly submitting unchanged pages or the entire site after unrelated edits.
This is a manual notification, not a browser script or an automatic deploy hook.

One request to `api.indexnow.org` is shared with participating search engines.
HTTP 200 confirms receipt; HTTP 202 means receipt with key validation pending.
Neither confirms indexing, ranking, or inclusion in an AI answer. IndexNow is
separate from Google Search Console submissions.
