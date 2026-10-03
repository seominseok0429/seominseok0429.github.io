// Include on individual posts after a <section data-blog-comments> element.
(() => {
  const target = document.querySelector('[data-blog-comments]');
  if (!target || target.querySelector('script[data-repo]')) return;
  const script = document.createElement('script');
  script.src = 'https://giscus.app/client.js';
  script.async = true;
  script.crossOrigin = 'anonymous';
  const config = {
    repo: 'seominseok0429/seominseok0429.github.io',
    'repo-id': 'R_kgDOQWrsdQ',
    category: 'Announcements',
    'category-id': 'DIC_kwDOQWrsdc4DG7Zj',
    mapping: 'pathname',
    strict: '1',
    'reactions-enabled': '1',
    'emit-metadata': '0',
    'input-position': 'top',
    theme: 'light',
    lang: 'ko',
    loading: 'lazy'
  };
  for (const [key, value] of Object.entries(config)) script.setAttribute(`data-${key}`, value);
  target.appendChild(script);
})();
