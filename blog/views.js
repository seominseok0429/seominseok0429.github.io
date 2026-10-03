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
  // Preserve an explicitly configured display count while still recording visits.
  if (display.hasAttribute('data-fixed-views')) return;

  const interval = 5 * 60 * 1000;
  let lastAttempt = 0;
  let pending = false;
  async function refresh() {
    if (pending || document.hidden || (lastAttempt && Date.now() - lastAttempt < interval)) return;
    pending = true;
    lastAttempt = Date.now();
    try {
      // Explicit dates give each day its own full-history counter request.
      // Start at the Unix epoch to include all visits; include today in Korea and UTC.
      const now = new Date();
      const end = new Date(now.getTime() + 9 * 60 * 60 * 1000).toISOString().slice(0, 10);
      const url = `${origin}/counter/${encodeURIComponent(path)}.json?start=1970-01-01&end=${end}`;
      const response = await fetch(url, { credentials: 'omit', cache: 'no-store' });
      if (!response.ok) throw new Error('View count unavailable');
      const data = await response.json();
      if (typeof data.count !== 'string' || !/^[0-9,.\s]+$/.test(data.count)) return;
      const lang = document.documentElement.lang;
      const label = lang === 'en' ? 'Views' : lang === 'zh-CN' ? '浏览量' : '조회수';
      display.textContent = `${label} ${data.count}`;
      display.title = lang === 'en' ? 'Actual GoatCounter visits. Checked every 5 minutes; provider caching may delay updates by up to 4 hours.' : lang === 'zh-CN' ? 'GoatCounter 实际访问统计。每 5 分钟检查一次；服务端缓存可能导致最多 4 小时的延迟。' : 'GoatCounter 실제 방문 집계. 5분마다 확인하며, 서비스 캐시로 최대 4시간 늦게 반영될 수 있습니다.';
      display.hidden = false;
    } catch (_) {
      // Keep the last successful count during a temporary network failure.
    } finally {
      pending = false;
    }
  }
  refresh();
  setInterval(refresh, interval);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
})();
