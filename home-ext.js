// Home page: a few community extensions, read live from /extensiones.json
// (the same catalog /extensiones shows), each card linking to that page.
// The section text is static HTML; without JavaScript only the button shows.
(function () {
  'use strict';
  const box = document.getElementById('home-ext-grid');
  if (!box) return;
  const lang = document.documentElement.lang.startsWith('pt') ? 'pt'
    : document.documentElement.lang.startsWith('en') ? 'en' : 'es';
  const page = { es: '/extensiones', en: '/en/extensiones', pt: '/pt/extensiones' }[lang];
  const by = { es: 'por', en: 'by', pt: 'por' }[lang];
  const SHOW = 6;

  function pick(texts) {
    if (!texts || typeof texts !== 'object') return '';
    return texts[lang] || texts.es || texts.en || texts.pt || '';
  }
  function el(tagName, cls, text) {
    const n = document.createElement(tagName);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function card(x) {
    const a = el('a', 'ext-card home-ext-card');
    a.href = page;
    const shot = el('div', 'ext-shot');
    if (typeof x.screenshot === 'string' && /^[a-z0-9_.-]+$/.test(x.screenshot)) {
      const img = document.createElement('img');
      img.src = '/extensiones-img/' + x.screenshot;
      img.alt = '';
      img.loading = 'lazy';
      img.width = 600;
      img.height = 375;
      shot.appendChild(img);
    } else {
      shot.classList.add('ext-shot-none');
      shot.appendChild(el('span', '', (pick(x.name) || '?').charAt(0).toUpperCase()));
    }
    a.appendChild(shot);
    const body = el('div', 'ext-body');
    body.appendChild(el('h3', '', pick(x.name)));
    body.appendChild(el('p', 'ext-author', `${by} ${x.author || ''}`));
    body.appendChild(el('p', 'ext-summary home-ext-summary', pick(x.summary)));
    a.appendChild(body);
    return a;
  }

  fetch('/extensiones.json', { cache: 'no-cache' })
    .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
    .then((data) => {
      const all = (Array.isArray(data) ? data : data.extensions) || [];
      // Those with a picture first, in a fresh order each visit.
      const shuffled = all
        .map((x) => [Math.random() - (x.screenshot ? 1 : 0), x])
        .sort((p, q) => p[0] - q[0])
        .map((p) => p[1]);
      shuffled.slice(0, SHOW).forEach((x) => box.appendChild(card(x)));
      const n = document.getElementById('home-ext-n');
      if (n && all.length) n.textContent = String(all.length);
    })
    .catch(() => { box.hidden = true; });
})();
