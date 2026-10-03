(() => {
  const site = document.currentScript.dataset.site;
  const display = document.querySelector('[data-post-views]');
  if (!site || !display || location.hostname !== 'seominseok0429.github.io') return;
  if (!/^[a-z0-9-]+$/.test(site)) return;
  const origin = `https://${site}.goatcounter.com`;
  const path = display.dataset.countPath || new URL(document.querySelector('link[rel="canonical"]').href).pathname;
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
      const lang = document.documentElement.lang;
      const label = lang === 'en' ? 'Views' : lang === 'zh-CN' ? '浏览量' : '조회수';
      display.textContent = `${label} ${data.count}`;
      display.title = lang === 'en' ? 'GoatCounter visits · Counts may take up to 4 hours to update.' : lang === 'zh-CN' ? 'GoatCounter 实际访问统计 · 显示更新可能需要最多 4 小时。' : 'GoatCounter 실제 방문 집계 · 표시 갱신에 최대 4시간이 걸릴 수 있습니다.';
      display.hidden = false;
    })
    .catch(() => { display.hidden = true; });
})();
