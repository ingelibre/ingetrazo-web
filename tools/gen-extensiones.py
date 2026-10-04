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
        "tags": "Filtrar por tema",
        "loading": "Cargando el catálogo…",
        "noscript": "Esta lista necesita JavaScript. También puedes ver el "
                    "catálogo directamente en",
        "install_h": "Cómo instalar",
        "install": [
            "Pulsa <strong>Descargar</strong> en la extensión. Recibes un "
            "archivo <code>.py</code> o un <code>.zip</code>.",
            "Si es un <code>.zip</code>, descomprímelo: queda una carpeta "
            "(por ejemplo <code>ja_sun</code>). Esa carpeta entera es la "
            "extensión: no saques los archivos de dentro.",
            "En IngeTrazo abre <strong>Extensiones ▸ Abrir carpeta de "
            "complementos</strong> y copia ahí el archivo <code>.py</code> "
            "o la carpeta.",
            "Cierra y vuelve a abrir IngeTrazo. La extensión aparece en el "
            "menú <strong>Extensiones</strong> o en el panel lateral. Si "
            "sale con ⚠, pasa el ratón por encima para ver el motivo.",
        ],
        "how": "¿Cómo se instalan?",
        "soon": "Pronto podrás instalarlas desde IngeTrazo con un clic.",
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
        "tags": "Filter by topic",
        "loading": "Loading the catalog…",
        "noscript": "This list needs JavaScript. You can also browse the "
                    "catalog directly at",
        "install_h": "How to install",
        "install": [
            "Click <strong>Download</strong> on the extension. You get a "
            "<code>.py</code> file or a <code>.zip</code>.",
            "If it is a <code>.zip</code>, unzip it: you get one folder "
            "(e.g. <code>ja_sun</code>). That whole folder is the "
            "extension — don't take the files out of it.",
            "In IngeTrazo open <strong>Extensions ▸ Open plugins "
            "folder</strong> and copy the <code>.py</code> file or the "
            "folder there.",
            "Close and reopen IngeTrazo. The extension shows up in the "
            "<strong>Extensions</strong> menu or in the side panel. If it "
            "has a ⚠, hover over it to see why.",
        ],
        "how": "How do I install one?",
        "soon": "Soon you will install them from inside IngeTrazo with one "
                "click.",
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
        "tags": "Filtrar por tema",
        "loading": "Carregando o catálogo…",
        "noscript": "Esta lista precisa de JavaScript. Você também pode ver o "
                    "catálogo diretamente em",
        "install_h": "Como instalar",
        "install": [
            "Clique em <strong>Baixar</strong> na extensão. Você recebe um "
            "arquivo <code>.py</code> ou um <code>.zip</code>.",
            "Se for um <code>.zip</code>, descompacte: fica uma pasta (por "
            "exemplo <code>ja_sun</code>). Essa pasta inteira é a extensão: "
            "não tire os arquivos de dentro.",
            "No IngeTrazo abra <strong>Extensões ▸ Abrir pasta de "
            "complementos</strong> e copie para lá o arquivo "
            "<code>.py</code> ou a pasta.",
            "Feche e abra de novo o IngeTrazo. A extensão aparece no menu "
            "<strong>Extensões</strong> ou no painel lateral. Se aparecer "
            "com ⚠, passe o mouse por cima para ver o motivo.",
        ],
        "how": "Como instalar?",
        "soon": "Em breve você poderá instalá-las de dentro do IngeTrazo com "
                "um clique.",
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

      <div class="ext-tools">
        <input type="search" id="ext-q" class="ext-search" placeholder="{t["search"]}" aria-label="{t["search"]}" autocomplete="off">
        <label class="ext-only"><input type="checkbox" id="ext-reviewed"> {t["only"]}</label>
      </div>
      <div class="ext-tags" id="ext-tags" role="group" aria-label="{t["tags"]}"></div>
      <p class="ext-count" id="ext-count" aria-live="polite">{t["loading"]}</p>
      <div class="ext-grid" id="ext-grid"></div>
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
