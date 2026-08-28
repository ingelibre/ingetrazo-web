#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""Turn Sweet Home 3D furniture libraries into the component library the
IngeTrazo tray browses.

A ``.sh3f`` is a ZIP: a ``PluginFurnitureCatalog*.properties`` catalogue plus
one folder per model holding its OBJ, its MTL and its images. This reads the
catalogue (Spanish names and categories, the base file for the paths), and
writes, per model:

* ``miniaturas/<id>.png`` — the icon the library already ships, 128 px. This
  is what the tray shows, so browsing costs kilobytes, not the model.
* ``modelos/<id>.zip`` — the OBJ with everything it needs beside it, so the
  download is one request and the import finds its textures.
* an entry in ``index.json`` — name, category, real size in centimetres,
  licence and author.

The size matters: the OBJs are written in CENTIMETRES, and the catalogue
declares each model's real width/depth/height, so the app never has to guess
the unit for these.

Usage:  gen-library.py <salida> <biblioteca.sh3f> [<biblioteca.sh3f> …]
"""
from __future__ import annotations

import collections
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

#: The licence each published Sweet Home 3D library carries, by the name its
#: archive uses. CC0 asks nothing; CC-BY needs the author credited, which is
#: why the author travels in the index; the Free Art License is copyleft, so
#: a derived work inherits it — the app has to be able to say which is which.
#: The name is written in English and the app translates it, like every
#: other string it shows — the index is data, not a Spanish document.
LICENCES = {
    "BlendSwap-CC-0": ("CC0-1.0", "Public domain"),
    "BlendSwap-CC-BY": ("CC-BY-4.0", "Creative Commons Attribution"),
    "Scopia": ("CC-BY-4.0", "Creative Commons Attribution"),
    "KatorLegaz": ("CC-BY-4.0", "Creative Commons Attribution"),
    "Reallusion": ("CC-BY-4.0", "Creative Commons Attribution"),
    "Contributions": ("LAL-1.3", "Free Art License"),
    "LucaPresidente": ("LAL-1.3", "Free Art License"),
    "Trees": ("LAL-1.3", "Free Art License"),
}


def _fields(text: str, tag: str) -> dict:
    return {int(i): v.strip()
            for i, v in re.findall(r"^%s#(\d+)=(.+)$" % tag, text, re.M)}


def _read(zf: zipfile.ZipFile, name: str) -> str:
    try:
        return zf.read(name).decode("iso-8859-1")
    except KeyError:
        return ""


def _licence_of(sh3f: Path) -> tuple[str, str]:
    stem = sh3f.stem
    for key, val in LICENCES.items():
        if key.lower() in stem.lower():
            return val
    return ("desconocida", "sin determinar")


#: An MTL names its images with these keys; the filename is the last token,
#: because the format lets options ("-s 1 1 1 pared.jpg") come first.
_MAP_KEYS = ("map_kd", "map_ka", "map_ks", "map_ke", "map_d", "map_bump",
             "map_ns", "bump", "refl", "disp", "decal")


def _beside(folder: str, ref: str, members: set) -> str | None:
    """Resolve a reference written inside an OBJ/MTL to a ZIP entry."""
    ref = ref.replace("\\", "/").lstrip("./")
    for cand in (folder + ref, folder + ref.rsplit("/", 1)[-1], ref):
        if cand in members:
            return cand
    return None


def _refs(text: str) -> list:
    """The files an OBJ or an MTL says it needs."""
    out = []
    for line in text.splitlines():
        parts = line.split()
        if not parts:
            continue
        key = parts[0].lower()
        if key not in _MAP_KEYS and key != "mtllib":
            continue
        if len(parts) > 1:
            # A name can carry spaces ("Six pack.mtl") and mtllib can list
            # several files, so offer both readings and let the archive say.
            out.append(line.split(None, 1)[1].strip())
            out.extend(parts[1:])
    return out


def _payload(zf, rel: str, folder: str, members: set) -> list:
    """The model's OBJ and only what it actually needs.

    Some collections give each model its own folder, and then the folder IS
    the model. Others drop hundreds of models loose in one folder, and there
    "everything beside it" would be the whole library — a hundred megabytes
    per model. So follow the references instead: the OBJ names its MTL, the
    MTL names its images.
    """
    need = [rel]
    seen = {rel}
    queue = [rel]
    while queue:
        cur = queue.pop()
        if not cur.lower().endswith((".obj", ".mtl")):
            continue
        for ref in _refs(zf.read(cur).decode("iso-8859-1", "replace")):
            got = _beside(folder, ref, members)
            if got and got not in seen:
                seen.add(got)
                need.append(got)
                queue.append(got)
    return need


def convert(sh3f: Path, out: Path, entries: list) -> int:
    """Add every model of ``sh3f`` to ``out``; returns how many were added."""
    spdx, licence_name = _licence_of(sh3f)
    collection = sh3f.stem
    with zipfile.ZipFile(sh3f) as zf:
        base = _read(zf, "PluginFurnitureCatalog.properties")
        es = _read(zf, "PluginFurnitureCatalog_es.properties") or base
        names = _fields(es, "name") or _fields(base, "name")
        names_en = _fields(base, "name")
        cats = _fields(es, "category") or _fields(base, "category")
        models, icons = _fields(base, "model"), _fields(base, "icon")
        widths, depths = _fields(base, "width"), _fields(base, "depth")
        heights, creators = _fields(base, "height"), _fields(base, "creator")
        rots = _fields(base, "modelRotation")
        members = set(zf.namelist())
        # A folder that holds a single model can travel whole; one shared by
        # many holds the whole collection and has to be followed by reference.
        owners = collections.Counter(
            models[i].lstrip("/").rsplit("/", 1)[0] + "/" for i in models)
        added = 0
        for i in sorted(models):
            rel = models[i].lstrip("/")
            if rel not in members:
                continue
            ident = "%s-%03d" % (collection.lower().replace("_", "-"), i)
            # The OBJ needs its MTL and its images beside it, so they all
            # travel in the same zip and the import finds them.
            folder = rel.rsplit("/", 1)[0] + "/"
            if owners[folder] == 1:
                payload = [m for m in members
                           if m.startswith(folder) and not m.endswith("/")]
            else:
                payload = _payload(zf, rel, folder, members)
            if not payload:
                continue
            (out / "modelos").mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(out / "modelos" / (ident + ".zip"), "w",
                                 zipfile.ZIP_DEFLATED) as dst:
                for m in payload:
                    dst.writestr(m.split("/")[-1], zf.read(m))
            icon = icons.get(i, "").lstrip("/")
            if icon in members:
                (out / "miniaturas").mkdir(parents=True, exist_ok=True)
                (out / "miniaturas" / (ident + ".png")).write_bytes(zf.read(icon))
            entries.append({
                "id": ident,
                "nombre": names.get(i, rel.rsplit("/", 1)[-1]),
                # The catalogue names every model in both languages and the
                # two agree one-to-one (unlike its categories), so the tray
                # can say "Washbasin" or "Lavabo" as the interface asks.
                "nombre_en": names_en.get(i, rel.rsplit("/", 1)[-1]),
                "categoria": cats.get(i, "Varios"),
                "coleccion": collection,
                "obj": rel.rsplit("/", 1)[-1],
                # Real size, straight from the catalogue: these OBJs are
                # written in centimetres and this is what they measure.
                "cm": [widths.get(i), depths.get(i), heights.get(i)],
                # Sweet Home 3D does not use the OBJ as it stands: it turns
                # it by this 3x3 (row-major, in the file's own Y-up space)
                # and then scales it to the size above. A quarter of these
                # models are written in arbitrary units, so both are needed
                # for a piece to arrive the size the catalogue promises.
                "rot": rots.get(i, "").split() or None,
                "licencia": spdx,
                "licencia_nombre": licence_name,
                "autor": creators.get(i, ""),
            })
            added += 1
    return added


def main(argv) -> int:
    if len(argv) < 3:
        print(__doc__.strip().splitlines()[-1])
        return 2
    out = Path(argv[1])
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    entries: list = []
    for src in argv[2:]:
        p = Path(src)
        n = convert(p, out, entries)
        print("  %-34s %4d modelos" % (p.name, n))
    index = {
        "version": 1,
        "unidad": "cm",
        "modelos": sorted(entries, key=lambda e: (e["categoria"], e["nombre"])),
    }
    (out / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    mb = sum(f.stat().st_size for f in out.rglob("*") if f.is_file()) / 1e6
    print("total: %d modelos, %.1f MB en %s" % (len(entries), mb, out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
