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
      all: 'Todas', updated: 'actualizada',
      more: (n) => `Ver más (${n})`, prev: 'Anteriores', next: 'Siguientes',
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
      all: 'All', updated: 'updated',
      more: (n) => `Show more (${n})`, prev: 'Previous', next: 'Next',
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
      all: 'Todas', updated: 'atualizada',
      more: (n) => `Ver mais (${n})`, prev: 'Anteriores', next: 'Próximas',
      tags: {
        architecture: 'Arquitetura', bim: 'BIM', structures: 'Estruturas',
        terrain: 'Terreno', drawing: 'Desenho', analysis: 'Análise',
        'import-export': 'Importar/exportar', rendering: 'Renderização',
        fabrication: 'Fabricação', productivity: 'Produtividade',
        education: 'Educação', other: 'Outras',
      },
    },
    ko: {
      download: '다운로드', code: '소스 코드', reviewed: '검토됨',
      community: '커뮤니티', by: '제작:', tested: 'IngeTrazo에서 테스트됨',
      count: (n, t) => n === t ? `확장 ${t}개` : `확장 ${t}개 중 ${n}개`,
      one: '확장 1개', none: '검색과 일치하는 확장이 없습니다.',
      error: '카탈로그를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.',
      all: '전체', updated: '업데이트',
      more: (n) => `더 보기 (${n})`, prev: '이전', next: '다음',
      tags: {
        architecture: '건축', bim: 'BIM', structures: '구조',
        terrain: '지형', drawing: '드로잉', analysis: '분석',
        'import-export': '가져오기/내보내기', rendering: '렌더링',
        fabrication: '제작', productivity: '생산성',
        education: '교육', other: '기타',
      },
    },
  };
  const ui = UI[lang] || UI.es;

  const q = document.getElementById('ext-q');
  const onlyReviewed = document.getElementById('ext-reviewed');
  const tagBox = document.getElementById('ext-tags');
  const count = document.getElementById('ext-count');
  const sortBy = document.getElementById('ext-sort');
  const more = document.getElementById('ext-more');
  // The full list shows a page at a time: with dozens of extensions a
  // single wall of cards buries the search box's results.
  const PAGE = 12;
  let limit = PAGE;
  let all = [];
  let tag = '';

  // The visitor's language, else Spanish, else English, else anything
  // (a Korean visitor gets English before Spanish).
  function pick(texts) {
    if (!texts || typeof texts !== 'object') return '';
    return texts[lang] || (lang === 'ko' && texts.en) || texts.es || texts.en || texts.pt || '';
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
      `v${x.version} · ${x.license} · ${ui.tested} ${x.ingetrazo}`
      + (day(x.updated_at) ? ` · ${ui.updated} ${day(x.updated_at)}` : '')));

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

  // «2026-10-15T15:48Z» (catalog.py, UTC) → the reader's own date format.
  function day(stamp) {
    const d = typeof stamp === 'string' ? new Date(stamp) : null;
    if (!d || isNaN(d)) return '';
    return d.toLocaleDateString(document.documentElement.lang || lang,
      { day: 'numeric', month: 'short', year: 'numeric' });
  }

  // The catalog's own order is «reviewed first, then by name»; the other
  // two sort a copy. An entry without dates (never merged) goes last.
  function sorted(list) {
    const mode = sortBy ? sortBy.value : '';
    if (mode === 'recent') {
      return [...list].sort((a, b) =>
        String(b.updated_at || '').localeCompare(String(a.updated_at || '')));
    }
    if (mode === 'name') {
      return [...list].sort((a, b) =>
        pick(a.name).localeCompare(pick(b.name), lang, { sensitivity: 'base' }));
    }
    return list;
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
    grid.replaceChildren(...sorted(shown).slice(0, limit).map(card));
    const left = shown.length - limit;
    if (more) {
      more.hidden = left <= 0;
      more.textContent = ui.more(left);
    }
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
        refilter();
      });
      return b;
    };
    tagBox.replaceChildren(make('', ui.all),
      ...[...used].sort((a, b) => (ui.tags[a] || a).localeCompare(ui.tags[b] || b))
        .map((t) => make(t, ui.tags[t] || t)));
  }

  // «Just added»: the latest merged entries in a strip that moves on by
  // itself until the visitor touches it (or asked for reduced motion).
  function carousel() {
    const box = document.getElementById('ext-new');
    const track = document.getElementById('ext-track');
    if (!box || !track) return;
    const recent = all.filter((x) => x.updated_at)
      .sort((a, b) => String(b.updated_at).localeCompare(String(a.updated_at)))
      .slice(0, 10);
    if (recent.length < 3) return;
    track.replaceChildren(...recent.map(card));
    box.hidden = false;
    const prev = document.getElementById('ext-prev');
    const next = document.getElementById('ext-next');
    prev.setAttribute('aria-label', ui.prev);
    next.setAttribute('aria-label', ui.next);
    const step = () => {
      const c = track.firstElementChild;
      return c ? c.getBoundingClientRect().width + 20 : track.clientWidth;
    };
    const atEnd = () => track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
    const edges = () => {
      prev.disabled = track.scrollLeft <= 4;
      next.disabled = atEnd();
    };
    track.addEventListener('scroll', edges, { passive: true });
    edges();

    let timer = null;
    const stop = () => { clearInterval(timer); timer = null; };
    prev.addEventListener('click', () => { stop(); track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    next.addEventListener('click', () => { stop(); track.scrollBy({ left: step(), behavior: 'smooth' }); });
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    let paused = false;
    ['pointerenter', 'focusin'].forEach((e) => box.addEventListener(e, () => { paused = true; }));
    ['pointerleave', 'focusout'].forEach((e) => box.addEventListener(e, () => { paused = false; }));
    ['pointerdown', 'wheel', 'keydown', 'touchstart'].forEach((e) =>
      track.addEventListener(e, stop, { passive: true }));
    timer = setInterval(() => {
      if (paused || document.hidden) return;
      if (atEnd()) track.scrollTo({ left: 0, behavior: 'smooth' });
      else track.scrollBy({ left: step(), behavior: 'smooth' });
    }, 5000);
  }

  const refilter = () => { limit = PAGE; render(); };
  q.addEventListener('input', refilter);
  onlyReviewed.addEventListener('change', refilter);
  if (sortBy) sortBy.addEventListener('change', refilter);
  if (more) more.addEventListener('click', () => { limit += PAGE; render(); });

  fetch('/extensiones.json', { headers: { Accept: 'application/json' } })
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((data) => {
      all = (data.extensions || []).filter((x) => x && typeof x === 'object');
      all.forEach((x) => { x._h = haystack(x); });
      chips();
      carousel();
      render();
    })
    .catch(() => { count.textContent = ui.error; });
})();
