// Idioma automático de ingetrazo.com.
//
// El sitio es estático (assets); este Worker solo corre para «/», «/apoyar»,
// «/firma» y «/extensiones» (run_worker_first en wrangler.jsonc) y decide si
// ese visitante se queda en español o va a /en/ o /pt/. Orden:
//   1. la cookie `lang` — elegir en el selector de la cabecera gana siempre;
//   2. el idioma preferido del navegador si es español o portugués;
//   3. el país (Cloudflare): Hispanoamérica y España → español,
//      Brasil y lusófonos → portugués;
//   4. todo lo demás (Alemania, China, EE. UU.…) → inglés.
// Los buscadores no se redirigen: ven el español y siguen los hreflang.
//
// También sirve el catálogo de extensiones (ver «Extensiones» más abajo).

const SPANISH = new Set([
  'AR', 'BO', 'CL', 'CO', 'CR', 'CU', 'DO', 'EC', 'ES', 'GQ', 'GT', 'HN',
  'MX', 'NI', 'PA', 'PE', 'PR', 'PY', 'SV', 'UY', 'VE',
]);
const PORTUGUESE = new Set(['AO', 'BR', 'CV', 'GW', 'MZ', 'PT', 'ST', 'TL']);
const SUPPORTED = new Set(['es', 'en', 'pt']);
const LANG_PAGES = new Set(['/', '/apoyar', '/firma', '/extensiones']);
const BOT = /bot|crawl|spider|slurp|facebookexternalhit|embedly|preview|whatsapp|telegram|discord|lighthouse/i;

export function firstLanguage(acceptLanguage) {
  const tags = (acceptLanguage || '')
    .split(',')
    .map((part, i) => {
      const [tag, ...params] = part.trim().split(';');
      const q = params.find((p) => p.trim().startsWith('q='));
      return { tag: tag.trim().toLowerCase(), q: q ? parseFloat(q.trim().slice(2)) || 0 : 1, i };
    })
    .filter((t) => t.tag && t.tag !== '*' && t.q > 0)
    .sort((a, b) => b.q - a.q || a.i - b.i);
  return tags.length ? tags[0].tag.slice(0, 2) : '';
}

export function pickLang({ cookie, acceptLanguage, country }) {
  const m = /(?:^|;\s*)lang=(es|en|pt)\b/.exec(cookie || '');
  if (m) return m[1];
  const browser = firstLanguage(acceptLanguage);
  if (browser === 'es' || browser === 'pt') return browser;
  if (SPANISH.has(country)) return 'es';
  if (PORTUGUESE.has(country)) return 'pt';
  return 'en';
}

// ---- Extensiones -------------------------------------------------------
// El catálogo vive en github.com/ingelibre/ingetrazo-extensions: aprobar
// una ficha allí actualiza ingetrazo.com/extensiones en minutos, sin
// desplegar. El Worker lo lee de GitHub (caché de 5 min) y, si GitHub no
// responde, sirve la copia `extensiones.json` que va con el sitio.
//   /extensiones.json            el catálogo
//   /extensiones-img/<archivo>   la captura de una extensión
//   /extensiones-descarga/<id>   el archivo de la extensión, SOLO si su
//                                SHA-256 es el aprobado en el catálogo
// Nada más se reenvía: no es un proxy abierto.

const CATALOG_RAW = 'https://raw.githubusercontent.com/ingelibre/ingetrazo-extensions/main/';
const MAX_DOWNLOAD = 5 * 1024 * 1024;
const IMG_TYPES = { png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', webp: 'image/webp' };

async function loadCatalog(request, env) {
  try {
    const r = await fetch(CATALOG_RAW + 'catalog.json', { cf: { cacheTtl: 300, cacheEverything: true } });
    if (r.ok) {
      const text = await r.text();
      const data = JSON.parse(text);
      if (Array.isArray(data.extensions)) return { text, data };
    }
  } catch (e) { /* GitHub caído o JSON roto: la copia local */ }
  const r = await env.ASSETS.fetch(new Request(new URL('/extensiones.json', request.url)));
  if (!r.ok) return null;
  const text = await r.text();
  return { text, data: JSON.parse(text) };
}

function plain(status, text) {
  return new Response(text, {
    status,
    headers: { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' },
  });
}

async function sha256Hex(buf) {
  const d = await crypto.subtle.digest('SHA-256', buf);
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export async function extensions(url, request, env) {
  const path = url.pathname;
  if (path === '/extensiones.json') {
    const cat = await loadCatalog(request, env);
    if (!cat) return plain(503, 'Catalog unavailable');
    return new Response(cat.text, {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=300',
      },
    });
  }
  let m = /^\/extensiones-img\/([a-z0-9_.-]+\.(png|jpe?g|webp))$/.exec(path);
  if (m) {
    const r = await fetch(CATALOG_RAW + 'screenshots/' + m[1], { cf: { cacheTtl: 86400, cacheEverything: true } });
    if (!r.ok) return plain(404, 'Not found');
    return new Response(r.body, {
      headers: { 'Content-Type': IMG_TYPES[m[2]], 'Cache-Control': 'public, max-age=86400' },
    });
  }
  m = /^\/extensiones-descarga\/([a-z][a-z0-9_]{1,47})$/.exec(path);
  if (m) {
    const cat = await loadCatalog(request, env);
    const entry = cat && cat.data.extensions.find((x) => x && x.id === m[1]);
    if (!entry) return plain(404, 'No such extension');
    const src = String(entry.download || '');
    if (!src.startsWith('https://')) return plain(404, 'No download');
    const r = await fetch(src, { cf: { cacheTtl: 3600, cacheEverything: true } });
    if (!r.ok) return plain(502, 'The author\'s file could not be downloaded.');
    const buf = await r.arrayBuffer();
    if (buf.byteLength > MAX_DOWNLOAD) return plain(502, 'File too large');
    if ((await sha256Hex(buf)) !== entry.sha256) {
      // El archivo del autor cambió después de aprobado: no se entrega.
      return plain(409, 'This file changed after it was approved in the catalog, '
        + 'so it is not served. / Este archivo cambió después de aprobarse en el '
        + 'catálogo; por seguridad no se entrega.');
    }
    const name = (src.split('/').pop() || entry.id).replace(/[^A-Za-z0-9_.-]/g, '_');
    return new Response(buf, {
      headers: {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': `attachment; filename="${name}"`,
        'Cache-Control': 'public, max-age=300',
      },
    });
  }
  return null;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith('/extensiones.json')
        || url.pathname.startsWith('/extensiones-')) {
      const res = await extensions(url, request, env);
      if (res) return res;
    }
    const ua = request.headers.get('User-Agent') || '';
    // Only the pages this Worker is for pick a language. A path the
    // assets do not have also reaches the Worker (Cloudflare's not-found
    // fallback): redirecting it to /en/<path> found nothing again and came
    // back here -- /en/en/en/..., the loop that broke Flatpak installs
    // outside Hispanoamerica (issue #167: optional delta-indexes files).
    if (LANG_PAGES.has(url.pathname) && !BOT.test(ua)) {
      const lang = pickLang({
        cookie: request.headers.get('Cookie'),
        acceptLanguage: request.headers.get('Accept-Language'),
        country: (request.cf && request.cf.country) || '',
      });
      if (SUPPORTED.has(lang) && lang !== 'es') {
        const path = url.pathname === '/' ? '/' : url.pathname;
        return new Response(null, {
          status: 302,
          headers: {
            Location: `/${lang}${path}${url.search}${url.hash}`,
            'Cache-Control': 'private, no-store',
            Vary: 'Accept-Language, Cookie',
          },
        });
      }
    }
    const res = await env.ASSETS.fetch(request);
    const out = new Response(res.body, res);
    out.headers.set('Vary', 'Accept-Language, Cookie');
    return out;
  },
};
