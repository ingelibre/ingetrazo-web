# IngeTrazo · Landing Page

Sitio web público de **IngeTrazo** (https://ingetrazo.com) — modelador 3D
libre para ingeniería y arquitectura. Hermano visual de
`~/ingepresupuestos-web` (ingepresupuestos.com): mismo stack, misma
estructura, mismas convenciones. **Ante la duda, el CLAUDE.md de aquel repo
es la referencia extendida.**

Repo del producto: `~/ingetrazo/` → github.com/tuxiasumari/ingetrazo (GPL-3.0).

## Stack (idéntico al hermano)

- HTML + CSS + JS vanilla, **sin build step**. Inter vía Google Fonts.
- Hosting: **Cloudflare Worker con assets estáticos** — PUBLICADO en
  https://ingetrazo.com desde 2026-07-16 (`wrangler.jsonc` + `.assetsignore`;
  deploy con `npx wrangler deploy`, ver `COMO-PUBLICAR.md`).
- `script.js`: versión desde **GitHub Releases API** (no R2 como el hermano),
  menú móvil, scroll reveal, lightbox, botón copiar.
- SEO: JSON-LD (SoftwareApplication + FAQPage — espejados con el HTML del
  FAQ), canonical, OG/Twitter (`images/og-banner.jpg` 1200×630), sitemap,
  robots. `_headers` con CSP (lista blanca: fonts + api.github.com).

## Identidad visual

Sistema de la familia Inge[X] con **acento por producto**:

- IngeTrazo = **Blueberry `#3689E6`** (`--accent`); IngePresupuestos = naranja.
- El naranja aparece SOLO en la sección puente «Del modelo al presupuesto».
- Secciones coloreadas: BIM = gradiente azul (la tesis), Terreno = lime suave
  `#F2F9EC`, puente = `--orange-soft`.
- Resto idéntico al hermano: header slate-700, impact slate-900, screenshots
  grandes alternando lado, español neutro (tuteo), "Ing. Marco Sumari".

## Screenshots (`images/screenshots/`)

Todas REALES, generadas por script contra la app en GL
(`QT_QPA_PLATFORM=xcb` + captura con `import -window` de ImageMagick —
`QWidget.grab()` NO captura el overlay QPainter del viewport):

- `principal.jpeg` — hero (copiada de `~/ingetrazo/docs/images/viewport.png`,
  recortada la franja inferior).
- `modelado.jpeg` — recorte del viewport del hero.
- `bim.jpeg` — casita taggeada + panel BIM con metrados (script scratch
  `shot_bim.py`; los números del panel se verificaron correctos).
- `terreno.jpeg` — terreno 3D del valle del Colca (Yanque) con Esri satelital.
- `import-sketchup.jpeg` — **plaza Yanque real abierta desde su .skp** (vía el
  conversor skp2dae bajo Wine): arco, bandera del Perú y empedrado con
  texturas, panel de materiales poblado. (Antes: vivero.dae con colores.)
- `laminas.jpeg` — **lámina A3 real exportada por IngeTrazo 0.3** (PDF de
  dogfooding `laminas-prueba/c3_a3_tecnica.pdf` → pdftoppm): planta +
  elevaciones de vivienda a 1:100, cajetín y escala gráfica. Candidata a
  reemplazo por una captura de la VENTANA del compositor cuando Marco la
  tome (mostraría los paneles y el flujo, no solo el resultado).

OG banner: `.cover-build/og.html` + Chromium headless (snap: solo escribe
dentro de $HOME) → `images/og-banner.jpg`.

## Decisiones (no revertir sin discutir)

- Sin frameworks, sin trackers, sin cookies banner.
- Descarga: cards por SO — Windows (instalador + zip; script.js resuelve las
  URLs exactas de los assets del release vía la API de GitHub) y Linux desde
  el código. AppImage pendiente.
- Sección SketchUp: `.skp` directo con instalador de un clic del conversor
  skp2dae (FAQ + JSON-LD espejados).
- Iterar local con `python3 -m http.server 8765`; publicar con
  `npx wrangler deploy` (Marco aprobó la publicación el 2026-07-16;
  cambios de contenido nuevos igual se muestran antes de desplegar).

## Contacto

Ing. Marco Sumari · ing.sumari@gmail.com · WhatsApp +51 998 839 090
