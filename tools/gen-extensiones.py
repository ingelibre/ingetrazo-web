#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""Write the extensions page in the site's three languages.

``extensiones.html``, ``en/extensiones.html`` and ``pt/extensiones.html``
take the header and the footer from the matching ``apoyar.html``, so the
navigation stays one thing to edit. The page itself is a shell: the cards
come from ``/extensiones.json`` (``extensiones.js``), which the Worker reads
from the catalog repository — approving an entry there updates the page
without a deploy. Run this only when the TEXT of the page changes.

Usage:  python3 tools/gen-extensiones.py
"""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = "https://github.com/ingelibre/ingetrazo-extensions"
GUIDE = "https://github.com/ingelibre/ingetrazo/blob/main/docs/plugins.md"
PAGES = {"es": ROOT, "en": ROOT / "en", "pt": ROOT / "pt"}
URL = {"es": "https://ingetrazo.com/extensiones",
       "en": "https://ingetrazo.com/en/extensiones",
       "pt": "https://ingetrazo.com/pt/extensiones"}
LOCALE = {"es": "es_PE", "en": "en_US", "pt": "pt_BR"}

T = {
    "es": {
        "title": "Extensiones · IngeTrazo",
        "desc": "Extensiones para IngeTrazo hechas por la comunidad: BIM, "
                "estructuras, terreno, dibujo y más. Libres, con su código "
                "a la vista.",
        "h1": "Extensiones",
        "lead": "Herramientas que la comunidad agrega a IngeTrazo. Todas son "
                "libres y su código está publicado; cada una se instala solo "
                "si la necesitas.",
        "search": "Buscar extensiones…",
        "only": "Solo revisadas",
        "sort": "Ordenar",
        "sort_default": "Revisadas primero",
        "sort_recent": "Más recientes",
        "sort_name": "Nombre (A–Z)",
        "tags": "Filtrar por tema",
        "loading": "Cargando el catálogo…",
        "noscript": "Esta lista necesita JavaScript. También puedes ver el "
                    "catálogo directamente en",
        "install_h": "Cómo instalar",
        "install": [
            'En IngeTrazo abre <strong>Extensiones ▸ Gestionar extensiones…</strong> (desde la versión 0.5.8).',
            'En la pestaña <strong>Explorar</strong> busca la extensión y pulsa <strong>Instalar</strong>. IngeTrazo la descarga, comprueba que sea exactamente el archivo aprobado y la activa.',
            'Si la extensión es de la comunidad, IngeTrazo te pregunta antes de instalarla. Las que ya tienes están en la pestaña <strong>Instaladas</strong>.',
        ],
        "how": "¿Cómo se instalan?",
        "soon": '¿Sin conexión o con una versión anterior? Pulsa <strong>Descargar</strong>, descomprime el <code>.zip</code>, copia la carpeta entera en <strong>Extensiones ▸ Abrir carpeta de extensiones</strong> y vuelve a abrir IngeTrazo.',
        "new_h": 'Recién llegadas',
        "all_h": 'Todas las extensiones',
        "safety_h": "Revisadas y de la comunidad",
        "reviewed": "Revisada",
        "reviewed_p": "alguien que mantiene IngeTrazo leyó el código de esa "
                      "versión exacta.",
        "community": "Comunidad",
        "community_p": "pasó la revisión automática, pero nadie leyó el "
                       "código a fondo. Instálala si confías en su autor.",
        "safety_note": "Una extensión es un programa con el mismo acceso a tu "
                       "computadora que IngeTrazo, igual que en Blender. El "
                       "botón Descargar comprueba que el archivo sea "
                       "exactamente el que se aprobó.",
        "publish_h": "¿Hiciste una extensión?",
        "publish_p": "Publícala aquí: se agrega con una ficha desde el "
                     "navegador, sin saber Git. Un robot la revisa en un "
                     "minuto y la página se actualiza sola.",
        "publish_btn": "Publicar mi extensión",
        "guide_btn": "Guía para escribir extensiones",
        "readme": "#español",
    },
    "en": {
        "title": "Extensions · IngeTrazo",
        "desc": "Community extensions for IngeTrazo: BIM, structures, "
                "terrain, drawing and more. Free, with their code in the "
                "open.",
        "h1": "Extensions",
        "lead": "Tools the community adds to IngeTrazo. All are free "
                "software with published code; install only the ones you "
                "need.",
        "search": "Search extensions…",
        "only": "Reviewed only",
        "sort": "Sort",
        "sort_default": "Reviewed first",
        "sort_recent": "Most recent",
        "sort_name": "Name (A–Z)",
        "tags": "Filter by topic",
        "loading": "Loading the catalog…",
        "noscript": "This list needs JavaScript. You can also browse the "
                    "catalog directly at",
        "install_h": "How to install",
        "install": [
            'In IngeTrazo open <strong>Extensions ▸ Manage extensions…</strong> (since version 0.5.8).',
            'In the <strong>Browse</strong> tab find the extension and click <strong>Install</strong>. IngeTrazo downloads it, checks it is exactly the approved file and turns it on.',
            'For a community extension, IngeTrazo asks you before installing it. The ones you have are in the <strong>Installed</strong> tab.',
        ],
        "how": "How do I install one?",
        "soon": 'Offline, or on an older version? Click <strong>Download</strong>, unzip the <code>.zip</code>, copy the whole folder into <strong>Extensions ▸ Open extensions folder</strong> and reopen IngeTrazo.',
        "new_h": 'Just added',
        "all_h": 'All extensions',
        "safety_h": "Reviewed and community",
        "reviewed": "Reviewed",
        "reviewed_p": "a maintainer of IngeTrazo read the code of that exact "
                      "version.",
        "community": "Community",
        "community_p": "passed the automatic check, but nobody read the code "
                       "in depth. Install it if you trust its author.",
        "safety_note": "An extension is a program with the same access to "
                       "your computer as IngeTrazo, as in Blender. The "
                       "Download button checks the file is exactly the one "
                       "that was approved.",
        "publish_h": "Made an extension?",
        "publish_p": "List it here with a short entry, from the browser, no "
                     "Git needed. A bot checks it in a minute and the page "
                     "updates by itself.",
        "publish_btn": "List my extension",
        "guide_btn": "Guide to writing extensions",
        "readme": "#english",
    },
    "pt": {
        "title": "Extensões · IngeTrazo",
        "desc": "Extensões da comunidade para o IngeTrazo: BIM, estruturas, "
                "terreno, desenho e mais. Livres, com o código aberto.",
        "h1": "Extensões",
        "lead": "Ferramentas que a comunidade acrescenta ao IngeTrazo. Todas "
                "são livres e têm o código publicado; instale só as que "
                "precisar.",
        "search": "Buscar extensões…",
        "only": "Só revisadas",
        "sort": "Ordenar",
        "sort_default": "Revisadas primeiro",
        "sort_recent": "Mais recentes",
        "sort_name": "Nome (A–Z)",
        "tags": "Filtrar por tema",
        "loading": "Carregando o catálogo…",
        "noscript": "Esta lista precisa de JavaScript. Você também pode ver o "
                    "catálogo diretamente em",
        "install_h": "Como instalar",
        "install": [
            'No IngeTrazo abra <strong>Extensões ▸ Gerenciar extensões…</strong> (desde a versão 0.5.8).',
            'Na aba <strong>Explorar</strong> procure a extensão e clique em <strong>Instalar</strong>. O IngeTrazo a baixa, confere que é exatamente o arquivo aprovado e a ativa.',
            'Se a extensão for da comunidade, o IngeTrazo pergunta antes de instalá-la. As que você já tem ficam na aba <strong>Instaladas</strong>.',
        ],
        "how": "Como instalar?",
        "soon": 'Sem conexão ou com uma versão anterior? Clique em <strong>Baixar</strong>, descompacte o <code>.zip</code>, copie a pasta inteira em <strong>Extensões ▸ Abrir pasta de extensões</strong> e abra o IngeTrazo de novo.',
        "new_h": 'Recém-chegadas',
        "all_h": 'Todas as extensões',
        "safety_h": "Revisadas e da comunidade",
        "reviewed": "Revisada",
        "reviewed_p": "um mantenedor do IngeTrazo leu o código dessa versão "
                      "exata.",
        "community": "Comunidade",
        "community_p": "passou na verificação automática, mas ninguém leu o "
                       "código a fundo. Instale se confiar no autor.",
        "safety_note": "Uma extensão é um programa com o mesmo acesso ao seu "
                       "computador que o IngeTrazo, como no Blender. O botão "
                       "Baixar confere que o arquivo é exatamente o aprovado.",
        "publish_h": "Fez uma extensão?",
        "publish_p": "Publique aqui com uma ficha, pelo navegador, sem saber "
                     "Git. Um robô a verifica em um minuto e a página se "
                     "atualiza sozinha.",
        "publish_btn": "Publicar minha extensão",
        "guide_btn": "Guia para escrever extensões",
        "readme": "#português",
    },
}


def head(lang: str) -> str:
    t = T[lang]
    alts = "\n".join(
        f'  <link rel="alternate" hreflang="{code}" href="{URL[code]}">'
        for code in ("es", "en", "pt"))
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#1A2434">

  <title>{e(t["title"])}</title>

  <meta name="description" content="{e(t["desc"])}">

  <link rel="canonical" href="{URL[lang]}">
{alts}
  <link rel="alternate" hreflang="x-default" href="{URL["es"]}">

  <meta property="og:site_name" content="IngeTrazo">
  <meta property="og:title" content="{e(t["title"])}">
  <meta property="og:description" content="{e(t["desc"])}">
  <meta property="og:image" content="https://ingetrazo.com/images/og-banner.jpg">
  <meta property="og:url" content="{URL[lang]}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{LOCALE[lang]}">

  <link rel="icon" href="/images/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="icon" href="/images/favicon-16.png" type="image/png" sizes="16x16">
  <link rel="apple-touch-icon" href="/images/logo.png" sizes="180x180">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/style.css">
</head>
"""


def main_section(lang: str) -> str:
    t = T[lang]
    steps = "\n".join(f"          <li>{s}</li>" for s in t["install"])
    return f"""  <!-- ============ EXTENSIONES ============ -->
  <!-- Generated by tools/gen-extensiones.py — edit the texts there. The
       cards are filled by /extensiones.js from /extensiones.json. -->
  <main class="section bg-light ext-page">
    <div class="container">
      <div class="section-head">
        <h1>{t["h1"]}</h1>
        <p>{t["lead"]} <a href="#instalar" class="ext-how">{t["how"]} ↓</a></p>
      </div>

      <section class="ext-new" id="ext-new" aria-labelledby="ext-new-h" hidden>
        <div class="ext-new-head">
          <h2 id="ext-new-h">{t["new_h"]}</h2>
          <div class="ext-new-nav">
            <button type="button" class="ext-nav" id="ext-prev" aria-label="←">‹</button>
            <button type="button" class="ext-nav" id="ext-next" aria-label="→">›</button>
          </div>
        </div>
        <div class="ext-track" id="ext-track" tabindex="0"></div>
      </section>

      <h2 class="ext-all-h" id="todas">{t["all_h"]}</h2>
      <div class="ext-tools">
        <input type="search" id="ext-q" class="ext-search" placeholder="{t["search"]}" aria-label="{t["search"]}" autocomplete="off">
        <label class="ext-only"><input type="checkbox" id="ext-reviewed"> {t["only"]}</label>
        <label class="ext-sort">{t["sort"]}
          <select id="ext-sort">
            <option value="">{t["sort_default"]}</option>
            <option value="recent">{t["sort_recent"]}</option>
            <option value="name">{t["sort_name"]}</option>
          </select>
        </label>
      </div>
      <div class="ext-tags" id="ext-tags" role="group" aria-label="{t["tags"]}"></div>
      <p class="ext-count" id="ext-count" aria-live="polite">{t["loading"]}</p>
      <div class="ext-grid" id="ext-grid"></div>
      <div class="ext-more-row"><button type="button" class="btn ext-more" id="ext-more" hidden></button></div>
      <noscript><p class="ext-empty">{t["noscript"]} <a href="{CATALOG}">{CATALOG.removeprefix("https://")}</a>.</p></noscript>

      <div class="ext-info">
        <div class="ext-box" id="instalar">
          <h2>{t["install_h"]}</h2>
          <ol>
{steps}
          </ol>
          <p class="ext-small">{t["soon"]}</p>
        </div>
        <div class="ext-box">
          <h2>{t["safety_h"]}</h2>
          <p><span class="ext-badge ext-badge-ok">{t["reviewed"]}</span> {t["reviewed_p"]}</p>
          <p><span class="ext-badge">{t["community"]}</span> {t["community_p"]}</p>
          <p class="ext-small">{t["safety_note"]}</p>
        </div>
        <div class="ext-box ext-box-cta" id="publicar">
          <h2>{t["publish_h"]}</h2>
          <p>{t["publish_p"]}</p>
          <a class="btn btn-primary" href="{CATALOG}{t["readme"]}" target="_blank" rel="noopener">{t["publish_btn"]}</a>
          <a class="ext-guide" href="{GUIDE}" target="_blank" rel="noopener">{t["guide_btn"]} →</a>
        </div>
      </div>
    </div>
  </main>

"""


def build(lang: str) -> str:
    src = (PAGES[lang] / "apoyar.html").read_text(encoding="utf-8")
    start = src.index("  <!-- ============ HEADER")
    end = src.index("  <!-- ============ APORTE")
    foot = src.index("  <!-- ============ FOOTER")
    header = src[start:end]
    prefix = "" if lang == "es" else f"/{lang}"
    header = header.replace(f'href="{prefix}/apoyar" hreflang',
                            f'href="{prefix}/extensiones" hreflang')
    for code in ("es", "en", "pt"):
        p = "" if code == "es" else f"/{code}"
        header = header.replace(f'href="{p}/apoyar" hreflang="{code}"',
                                f'href="{p}/extensiones" hreflang="{code}"')
    footer = src[foot:].replace(
        '  <script src="/script.js"></script>',
        '  <script src="/script.js"></script>\n'
        '  <script src="/extensiones.js"></script>')
    return head(lang) + "<body>\n\n" + header + main_section(lang) + footer


def main() -> None:
    for lang, folder in PAGES.items():
        out = folder / "extensiones.html"
        out.write_text(build(lang), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
