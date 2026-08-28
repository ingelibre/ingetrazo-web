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

Renovadas COMPLETAS el 2026-08-08 con capturas manuales de Marco (fuente:
`~/Imágenes/Capturas de pantalla/ingetrazo/`, convertidas a JPEG 1600px):

- `principal.jpeg` — hero: **coso taurino con andenería**, graderías, arcos,
  toros y público; paneles de capas/escenas/materiales.
- `modelado.jpeg` — caseta de ladrillo con Empujar/Tirar activo y VCB.
- `bim.jpeg` — nave industrial (tijerales + cobertura curva) con el panel
  Tagging BIM (IfcColumn) abierto.
- `terreno.jpeg` — **levantamiento de dron real de un valle** con ruta
  trazada, perfil longitudinal abierto y lectura UTM en barra de estado
  (marco de ventana GNOME recortado con -trim, fondo #1e242c).
- `import-sketchup.jpeg` — parque infantil abierto desde su `.skp` con las
  capas originales de SketchUp (PERIMETRO, TREES, people…).
- `laminas.jpeg` — **lámina A3 real exportada por IngeTrazo 0.3** (PDF de
  dogfooding `laminas-prueba/c3_a3_tecnica.pdf` → pdftoppm): planta +
  elevaciones de vivienda a 1:100, cajetín y escala gráfica. Candidata a
  reemplazo por una captura de la VENTANA del compositor cuando Marco la
  tome (mostraría los paneles y el flujo, no solo el resultado).

OG banner: `.cover-build/og.html` + Chromium headless (snap: solo escribe
dentro de $HOME) → `images/og-banner.jpg`.

## Biblioteca de componentes (`biblioteca/`) — 1.510 modelos, 185 MB

Lo que la bandeja «Más componentes…» de IngeTrazo navega. **No está en git**:
son datos DERIVADOS, y su sitio es el despliegue, no el historial.

- **Se regenera en ~23 s** desde las bibliotecas de muebles de Sweet Home 3D
  (`.sh3f`, que son ZIP), descargables de sweethome3d.com:

  ```
  python3 tools/gen-library.py biblioteca \
      <BlendSwap-CC-0.sh3f> <Contributions.sh3f> <Scopia.sh3f> \
      <BlendSwap-CC-BY.sh3f> <KatorLegaz.sh3f> <LucaPresidente.sh3f> \
      <Reallusion.sh3f> <Trees.sh3f>
  ```

  Produce `index.json` (456 KB), `miniaturas/<id>.png` (18 MB) y
  `modelos/<id>.zip` (167 MB). El índice lleva, por modelo, su nombre y
  categoría en español, su **tamaño real en cm**, su licencia y su autor —
  la mezcla es CC0, CC-BY y Arte Libre (copyleft), y la app las muestra.

- **Cloudflare la publica gratis**: los assets estáticos de un Worker no
  cobran peticiones ni tráfico, y el plan libre admite 20.000 archivos de
  hasta 25 MiB. Nosotros ponemos 3.021 y el mayor pesa 2,6 MB.
- Está en `.gitignore` pero **NO en `.assetsignore`**: git la ignora,
  wrangler la sube. No invertir eso.
- La app la lee de `https://ingetrazo.com/biblioteca`
  (`app/core/library.py`, `DEFAULT_URL`; `$INGETRAZO_LIBRARY` lo sustituye
  por una carpeta o una URL para probar). Navegar cuesta kilobytes: solo se
  descarga el modelo que se pulsa, y queda en caché.

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
