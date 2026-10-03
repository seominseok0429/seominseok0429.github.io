(() => {
  const site = document.currentScript.dataset.site;
  const display = document.querySelector('[data-post-views]');
  if (!site || !display || location.hostname !== 'seominseok0429.github.io') return;
  if (!/^[a-z0-9-]+$/.test(site)) return;
  const origin = `https://${site}.goatcounter.com`;
  const path = new URL(document.querySelector('link[rel="canonical"]').href).pathname;
  window.goatcounter = { path };
  const tracker = document.createElement('script');
  tracker.src = 'https://gc.zgo.at/count.js';
  tracker.dataset.goatcounter = `${origin}/count`;
  tracker.async = true;
  document.head.appendChild(tracker);
  fetch(`${origin}/counter/${encodeURIComponent(path)}.json`, { credentials: 'omit' })
    .then(response => {
      if (!response.ok) throw new Error('View count unavailable');
      return response.json();
    })
    .then(data => {
      if (typeof data.count !== 'string' || !/^[0-9,.\s]+$/.test(data.count)) return;
      display.textContent = `조회수 ${data.count}`;
      display.title = '조회수는 주기적으로 갱신됩니다.';
      display.hidden = false;
    })
    .catch(() => { display.hidden = true; });
})();
