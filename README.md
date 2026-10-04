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
