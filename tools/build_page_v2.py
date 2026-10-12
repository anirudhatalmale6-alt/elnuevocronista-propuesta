#!/usr/bin/env python3
"""Version 2 de la propuesta: MAS NOTAS EN CADA SECCION (pedido de Javier).

Usa las ultimas 14 notas reales de cada categoria (data/secciones.json, API
publica de WordPress). Cabecera, apertura, lateral, avisos y pie son los mismos
de la v1: se reutiliza build_page.armar(); aca solo cambia la columna principal.

Cada seccion: 1 destacada + 3 en lista con miniatura + 4 en grilla + titulares
sin foto. Los titulares de texto suman notas sin sumar peso ni demasiado alto.
"""
import io
import json
import os
import urllib.request

from PIL import Image

import build_page as bp

BASE = bp.BASE
SECC = json.load(open(os.path.join(BASE, "data", "secciones.json")))
IMGDIR = os.path.join(BASE, "assets", "img", "notas")
UA = {"User-Agent": "Mozilla/5.0"}

# orden, rotulo y cuantas notas muestra cada seccion
SECCIONES = [
    ("la-ciudad", "La Ciudad", 10),
    ("politica", "Política", 10),
    ("deportes", "Deportes", 12),
    ("policiales", "Seguridad", 10),
    ("cultura", "Cultura", 10),
    ("sociedad", "Sociedad", 10),
    ("salud", "Salud", 6),
    ("provinciales", "Provinciales", 6),
]
# ancho de archivo = 2x del ancho en pantalla (nitido en celulares)
ANCHO = {"grande": 1000, "lista": 260, "tarjeta": 460}
# cabecera de seccion seguida de aviso horizontal, como en la v1
AVISO_DESPUES = {"politica": 2, "deportes": 3, "policiales": 4, "cultura": 5}


def foto(post, rol):
    """Devuelve (src, w, h) de la imagen de la nota al tamano del rol; la genera si falta."""
    w = ANCHO[rol]
    name = f"s{post['id']}-{w}.webp"
    path = os.path.join(IMGDIR, name)
    if not os.path.exists(path):
        raw = urllib.request.urlopen(urllib.request.Request(post["img"], headers=UA), timeout=40).read()
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(path, "WEBP", quality=80, method=6)
    with Image.open(path) as im:
        return f"assets/img/notas/{name}", im.width, im.height


def tarjeta(post, rol, cls="", bajada=False, largo=200):
    src, w, h = foto(post, rol)
    b = f'<p class="bajada">{bp.esc(bp.corta(post["bajada"], largo))}</p>' if bajada and post["bajada"] else ""
    return (f'<article class="nota {cls}"><a class="nota__img" href="{post["link"]}">'
            f'<img src="{src}" width="{w}" height="{h}" alt="{bp.esc(post["titulo"])}" loading="lazy" decoding="async"></a>'
            f'<div class="nota__txt"><h3><a href="{post["link"]}">{bp.esc(post["titulo"])}</a></h3>{b}'
            f'<p class="meta">{bp.fecha(post["fecha"])}</p></div></article>')


def titular(post):
    return (f'<li><a href="{post["link"]}">{bp.esc(post["titulo"])}</a>'
            f'<span>{bp.fecha(post["fecha"])}</span></li>')


def bloque(posts, chico=False):
    if chico:   # salud / provinciales: grilla de 4 + titulares
        return (f'<div class="g-4">{"".join(tarjeta(p, "tarjeta") for p in posts[:4])}</div>'
                f'<ul class="titulares">{"".join(titular(p) for p in posts[4:])}</ul>')
    grande, lista, grilla, resto = posts[0], posts[1:4], posts[4:8], posts[8:]
    return (f'<div class="g-1l">{tarjeta(grande, "grande", "nota--gr", bajada=True)}'
            f'<div class="lista">{"".join(tarjeta(p, "lista") for p in lista)}</div></div>'
            f'<div class="g-4 fila">{"".join(tarjeta(p, "tarjeta") for p in grilla)}</div>'
            f'<ul class="titulares">{"".join(titular(p) for p in resto)}</ul>')


def principal_v2():
    # lo que ya esta en la apertura no se repite en las secciones
    usados = {bp.N[i]["id"] for i in (16, 4, 3, 1)}
    partes, total = [], 0
    for slug, rotulo, cuantas in SECCIONES:
        elegidas = []
        for p in SECC[slug]:
            if p["id"] in usados or not p["img"]:
                continue
            elegidas.append(p)
            usados.add(p["id"])          # una nota que esta en dos categorias aparece una sola vez
            if len(elegidas) == cuantas:
                break
        if len(elegidas) < cuantas:
            print(f"  aviso: {slug} tiene {len(elegidas)} de {cuantas} notas")
        total += len(elegidas)
        partes.append(bp.sec(rotulo, slug, bloque(elegidas, chico=cuantas <= 6)))
        if slug in AVISO_DESPUES:
            partes.append(bp.aviso(bp.H[AVISO_DESPUES[slug]]))
    print(f"notas en las secciones: {total}")
    return "\n".join(partes)


if __name__ == "__main__":
    os.makedirs(IMGDIR, exist_ok=True)
    bp.armar(principal_v2(), "mas-noticias.html",
             "El Nuevo Cronista — Propuesta con más noticias por sección")
