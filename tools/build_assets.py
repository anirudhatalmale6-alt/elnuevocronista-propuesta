#!/usr/bin/env python3
"""Prepara las imagenes de la propuesta de portada de El Nuevo Cronista.

- Notas: baja la imagen destacada de cada nota elegida y la deja en WebP al
  doble del ancho en que se muestra (nitida en pantallas retina).
- Avisos: los 31 avisos reales de la portada. Los estaticos van a WebP; los GIF
  animados a WebP animado, conservando todos los cuadros y sus tiempos.

Las originales quedan en assets/src/ y no se tocan.
"""
import io
import json
import os
import urllib.request

from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "assets", "src")
OUT = os.path.join(BASE, "assets", "img")
AVISOS_SRC = os.path.join(SRC, "avisos")
UA = {"User-Agent": "Mozilla/5.0"}

# indice en data/notas.json -> ancho final en px (2x del ancho en pantalla)
NOTAS = {
    16: 1400,                                   # nota principal
    4: 720, 3: 720, 1: 720,                     # columna derecha de apertura
    34: 720, 30: 720, 22: 720, 56: 720,         # La ciudad
    28: 720, 41: 720, 31: 720, 18: 720,         # Politica
    26: 1000, 14: 720, 8: 720, 12: 720, 10: 720, 43: 720,   # Deportes
    0: 720, 44: 720, 49: 720, 19: 720,          # Seguridad
    29: 1000, 2: 720, 13: 720, 21: 720,         # Cultura
    25: 720, 24: 720, 27: 720, 55: 720,         # Sociedad
}


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()


def webp_static(im, width, path, q=80):
    im = im.convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(path, "WEBP", quality=q, method=6)
    return im.size


def webp_animated(src_path, width, path, q=78):
    """GIF animado -> WebP animado, mismo numero de cuadros y mismos tiempos."""
    g = Image.open(src_path)
    frames, durations = [], []
    for i in range(g.n_frames):
        g.seek(i)
        f = g.convert("RGBA")
        if f.width > width:
            f = f.resize((width, round(f.height * width / f.width)), Image.LANCZOS)
        frames.append(f)
        durations.append(g.info.get("duration", 100))
    frames[0].save(path, "WEBP", save_all=True, append_images=frames[1:],
                   duration=durations, loop=g.info.get("loop", 0), quality=q, method=6)
    return frames[0].size, len(frames)


def main():
    os.makedirs(os.path.join(OUT, "notas"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "avisos"), exist_ok=True)
    notas = json.load(open(os.path.join(BASE, "data", "notas.json")))

    antes = despues = 0
    manifest = {}
    for idx, width in NOTAS.items():
        n = notas[idx]
        raw = fetch(n["img"])
        dest = os.path.join(OUT, "notas", f"n{n['id']}.webp")
        size = webp_static(Image.open(io.BytesIO(raw)), width, dest)
        antes += len(raw)
        despues += os.path.getsize(dest)
        manifest[idx] = {"id": n["id"], "src": f"assets/img/notas/n{n['id']}.webp",
                         "w": size[0], "h": size[1]}
    print(f"notas: {len(NOTAS)} imagenes  {antes/1024/1024:.2f} MB -> {despues/1024/1024:.2f} MB")

    a_antes = a_despues = 0
    avisos = {}
    for f in sorted(os.listdir(AVISOS_SRC)):
        sp = os.path.join(AVISOS_SRC, f)
        im = Image.open(sp)
        ratio = im.width / im.height
        forma = "horizontal" if ratio > 2.2 else ("vertical" if ratio < 0.85 else "cuadrado")
        width = 1200 if forma == "horizontal" else 680
        name = os.path.splitext(f)[0] + ".webp"
        dest = os.path.join(OUT, "avisos", name)
        if getattr(im, "n_frames", 1) > 1:
            size, nfr = webp_animated(sp, width, dest)
        else:
            size, nfr = webp_static(im, width, dest), 1
        a_antes += os.path.getsize(sp)
        a_despues += os.path.getsize(dest)
        avisos[f] = {"src": f"assets/img/avisos/{name}", "w": size[0], "h": size[1],
                     "forma": forma, "cuadros": nfr}
    print(f"avisos: {len(avisos)} imagenes  {a_antes/1024/1024:.2f} MB -> {a_despues/1024/1024:.2f} MB")

    tapa = Image.open(os.path.join(SRC, "TAPA.jpg"))
    webp_static(tapa, 560, os.path.join(OUT, "tapa-1678.webp"), q=82)

    json.dump({"notas": manifest, "avisos": avisos},
              open(os.path.join(BASE, "data", "imagenes.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
