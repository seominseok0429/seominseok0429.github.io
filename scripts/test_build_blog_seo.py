"""Run with: python3 -m unittest discover -s scripts -p 'test_*.py'."""
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


class BuildBlogSeoTest(unittest.TestCase):
    def test_regeneration_is_stable_and_preserves_visible_content(self):
        origin = 'https://seominseok0429.github.io'
        article = '/blog/posts/when-ai-believes-a-false-reality/'
        for existing_block in (True, False):
            with self.subTest(existing_block=existing_block), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / 'scripts').mkdir()
                shutil.copyfile(Path(__file__).with_name('build-blog-seo.py'),
                                root / 'scripts/build-blog-seo.py')
                page = root / article.lstrip('/') / 'index.html'
                page.parent.mkdir(parents=True)
                old_block = ('<!-- SEO:START -->\n<meta name="robots" content="noindex">\n'
                             '<!-- SEO:END -->\n') if existing_block else ''
                source = ('<!doctype html>\n<html lang="ko">\n<head>\n'
                          '<title>Example post</title>\n'
                          '<meta name="description" content="Old description">\n'
                          f'<link rel="canonical" href="{origin}{article}">\n'
                          f'<link rel="alternate" hreflang="ko" href="{origin}{article}">\n'
                          '<!-- Keep this spacing and head order. -->\n\n'
                          + old_block + '<link rel="icon" href="/favicon.svg">\n</head>\n'
                          '<body class="article">\n<h1>Example <em>post</em></h1>\n'
                          '<div class="post-meta"><time datetime="2026-10-03">2026. 10. 03.</time></div>\n'
                          '<main class="post-body"><p>본문 &amp; preserved whitespace.</p>\n'
                          '<video controls src="example.mp4"></video></main>\n</body>\n</html>\n')
                page.write_text(source, encoding='utf-8')
                env = dict(os.environ, GIT_AUTHOR_DATE='2026-10-06T12:00:00+0900',
                           GIT_COMMITTER_DATE='2026-10-06T12:00:00+0900')
                for command in (['git', 'init', '-q'], ['git', 'add', 'blog'],
                                ['git', '-c', 'user.name=SEO test', '-c', 'user.email=seo@example.invalid',
                                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Fixture']):
                    subprocess.run(command, cwd=root, env=env, check=True, capture_output=True)

                def generate():
                    subprocess.run([sys.executable, 'scripts/build-blog-seo.py'], cwd=root,
                                   check=True, capture_output=True)
                    return {name: (root / name).read_bytes() for name in (
                        str(page.relative_to(root)), 'sitemap.xml', 'sitemap.txt',
                        'robots.txt', 'blog/feed.xml')}

                first = generate()
                second = generate()
                self.assertEqual(first, second, 'Repeated builds must not add whitespace or change metadata.')
                rendered = page.read_text(encoding='utf-8')
                self.assertEqual(source[source.index('<body'):], rendered[rendered.index('<body'):])
                self.assertEqual(rendered.count('<!-- SEO:START -->'), 1)
                self.assertNotIn('content="noindex"', rendered)
                if existing_block:
                    # Existing metadata stays before the icon; surrounding whitespace stays intact.
                    before_marker = source[:source.index('<!-- SEO:START -->')]
                    new_before_marker = rendered[:rendered.index('<!-- SEO:START -->')]
                    normalize_description = lambda value: re.sub(r'<meta name="description"[^>]*>', '', value)
                    self.assertEqual(normalize_description(before_marker), normalize_description(new_before_marker))
                    self.assertEqual(source.split('<!-- SEO:END -->', 1)[1],
                                     rendered.split('<!-- SEO:END -->', 1)[1])


if __name__ == '__main__':
    unittest.main()
