// Página de extensiones: dibuja las tarjetas desde /extensiones.json.
//
// El JSON lo sirve worker.js, que lo lee del repositorio del catálogo
// (github.com/ingelibre/ingetrazo-extensions): aprobar una ficha allí
// actualiza esta página sin publicar nada. Todo lo que viene del catálogo
// se escribe con textContent — una ficha nunca puede inyectar HTML.

(function () {
  'use strict';

  const grid = document.getElementById('ext-grid');
  if (!grid) return;
  const lang = (document.documentElement.lang || 'es').slice(0, 2);

  const UI = {
    es: {
      download: 'Descargar', code: 'Ver código', reviewed: 'Revisada',
      community: 'Comunidad', by: 'por', tested: 'Probada con IngeTrazo',
      count: (n, t) => n === t ? `${t} extensiones` : `${n} de ${t} extensiones`,
      one: '1 extensión', none: 'Ninguna extensión coincide con la búsqueda.',
      error: 'No se pudo cargar el catálogo. Inténtalo de nuevo en un momento.',
      all: 'Todas',
      tags: {
        architecture: 'Arquitectura', bim: 'BIM', structures: 'Estructuras',
        terrain: 'Terreno', drawing: 'Dibujo', analysis: 'Análisis',
        'import-export': 'Importar/exportar', rendering: 'Render',
        fabrication: 'Fabricación', productivity: 'Productividad',
        education: 'Educación', other: 'Otras',
      },
    },
    en: {
      download: 'Download', code: 'Source code', reviewed: 'Reviewed',
      community: 'Community', by: 'by', tested: 'Tested with IngeTrazo',
      count: (n, t) => n === t ? `${t} extensions` : `${n} of ${t} extensions`,
      one: '1 extension', none: 'No extension matches the search.',
      error: 'The catalog could not be loaded. Please try again shortly.',
      all: 'All',
      tags: {
        architecture: 'Architecture', bim: 'BIM', structures: 'Structures',
        terrain: 'Terrain', drawing: 'Drawing', analysis: 'Analysis',
        'import-export': 'Import/export', rendering: 'Rendering',
        fabrication: 'Fabrication', productivity: 'Productivity',
        education: 'Education', other: 'Other',
      },
    },
    pt: {
      download: 'Baixar', code: 'Ver código', reviewed: 'Revisada',
      community: 'Comunidade', by: 'por', tested: 'Testada com IngeTrazo',
      count: (n, t) => n === t ? `${t} extensões` : `${n} de ${t} extensões`,
      one: '1 extensão', none: 'Nenhuma extensão corresponde à busca.',
      error: 'Não foi possível carregar o catálogo. Tente de novo em instantes.',
      all: 'Todas',
      tags: {
        architecture: 'Arquitetura', bim: 'BIM', structures: 'Estruturas',
        terrain: 'Terreno', drawing: 'Desenho', analysis: 'Análise',
        'import-export': 'Importar/exportar', rendering: 'Renderização',
        fabrication: 'Fabricação', productivity: 'Produtividade',
        education: 'Educação', other: 'Outras',
      },
    },
  };
  const ui = UI[lang] || UI.es;

  const q = document.getElementById('ext-q');
  const onlyReviewed = document.getElementById('ext-reviewed');
  const tagBox = document.getElementById('ext-tags');
  const count = document.getElementById('ext-count');
  let all = [];
  let tag = '';

  // The visitor's language, else Spanish, else English, else anything.
  function pick(texts) {
    if (!texts || typeof texts !== 'object') return '';
    return texts[lang] || texts.es || texts.en || texts.pt || '';
  }

  function safeUrl(u) {
    return typeof u === 'string' && u.startsWith('https://') ? u : null;
  }

  function el(tagName, cls, text) {
    const n = document.createElement(tagName);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function card(x) {
    const c = el('article', 'ext-card');
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
    c.appendChild(shot);

    const body = el('div', 'ext-body');
    const top = el('div', 'ext-top');
    top.appendChild(el('h3', '', pick(x.name)));
    top.appendChild(el('span', x.reviewed ? 'ext-badge ext-badge-ok' : 'ext-badge',
      x.reviewed ? ui.reviewed : ui.community));
    body.appendChild(top);
    body.appendChild(el('p', 'ext-author', `${ui.by} ${x.author || ''}`));
    body.appendChild(el('p', 'ext-summary', pick(x.summary)));

    const tags = el('div', 'ext-card-tags');
    (x.tags || []).forEach((t) => tags.appendChild(el('span', '', ui.tags[t] || t)));
    body.appendChild(tags);

    body.appendChild(el('p', 'ext-meta',
      `v${x.version} · ${x.license} · ${ui.tested} ${x.ingetrazo}`));

    const links = el('div', 'ext-links');
    if (/^[a-z][a-z0-9_]*$/.test(x.id || '')) {
      const dl = el('a', 'btn btn-primary btn-sm', ui.download);
      // Through the Worker: it checks the SHA-256 against the catalog and
      // hands the file over as a download, not as text in the browser.
      dl.href = '/extensiones-descarga/' + x.id;
      dl.rel = 'nofollow';
      links.appendChild(dl);
    }
    const repo = safeUrl(x.repository);
    if (repo) {
      const a = el('a', 'ext-code', ui.code + ' →');
      a.href = repo;
      a.target = '_blank';
      a.rel = 'noopener nofollow';
      links.appendChild(a);
    }
    body.appendChild(links);
    c.appendChild(body);
    return c;
  }

  function haystack(x) {
    const parts = [x.id, x.author];
    ['name', 'summary'].forEach((k) => {
      if (x[k] && typeof x[k] === 'object') parts.push(...Object.values(x[k]));
    });
    (x.tags || []).forEach((t) => parts.push(t, ui.tags[t] || ''));
    return parts.join(' ').toLowerCase()
      .normalize('NFD').replace(/[̀-ͯ]/g, '');
  }

  function render() {
    const words = (q.value || '').toLowerCase()
      .normalize('NFD').replace(/[̀-ͯ]/g, '')
      .split(/\s+/).filter(Boolean);
    const shown = all.filter((x) =>
      (!onlyReviewed.checked || x.reviewed) &&
      (!tag || (x.tags || []).includes(tag)) &&
      words.every((w) => x._h.includes(w)));
    grid.replaceChildren(...shown.map(card));
    if (!shown.length) {
      count.textContent = ui.none;
    } else {
      count.textContent = all.length === 1 ? ui.one : ui.count(shown.length, all.length);
    }
  }

  function chips() {
    const used = new Set();
    all.forEach((x) => (x.tags || []).forEach((t) => used.add(t)));
    const make = (value, label) => {
      const b = el('button', 'ext-chip', label);
      b.type = 'button';
      b.setAttribute('aria-pressed', String(tag === value));
      b.addEventListener('click', () => {
        tag = value;
        tagBox.querySelectorAll('.ext-chip').forEach((o) =>
          o.setAttribute('aria-pressed', String(o === b)));
        render();
      });
      return b;
    };
    tagBox.replaceChildren(make('', ui.all),
      ...[...used].sort((a, b) => (ui.tags[a] || a).localeCompare(ui.tags[b] || b))
        .map((t) => make(t, ui.tags[t] || t)));
  }

  q.addEventListener('input', render);
  onlyReviewed.addEventListener('change', render);

  fetch('/extensiones.json', { headers: { Accept: 'application/json' } })
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((data) => {
      all = (data.extensions || []).filter((x) => x && typeof x === 'object');
      all.forEach((x) => { x._h = haystack(x); });
      chips();
      render();
    })
    .catch(() => { count.textContent = ui.error; });
})();
