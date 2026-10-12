#!/usr/bin/env python3
"""Arma index.html de la propuesta con las notas y los avisos REALES del sitio.

Fuente: data/notas.json (API publica de WordPress) y data/imagenes.json
(generado por build_assets.py). No se inventa ningun titulo ni ningun aviso.
"""
import html
import json
import os
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = json.load(open(os.path.join(BASE, "data", "notas.json")))
IMG = json.load(open(os.path.join(BASE, "data", "imagenes.json")))
FOTO = {int(k): v for k, v in IMG["notas"].items()}
AV = IMG["avisos"]

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
# el menu de hoy llama "Seguridad" a la categoria Policiales: se respeta
ROTULO = {"Policiales": "Seguridad", "La ciudad": "La Ciudad"}


def esc(s):
    return html.escape(s, quote=True)


def fecha(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month - 1]}"


def corta(texto, maximo):
    """Recorta una bajada sin partir palabras.

    Prefiere terminar en el ultimo punto antes del maximo (oracion completa);
    si no hay ninguno razonable, corta en la ultima palabra entera y pone "…".
    """
    texto = texto.strip()
    if len(texto) <= maximo:
        return texto
    trozo = texto[:maximo]
    # solo ". " cuenta como fin de oracion: un "." suelto puede ser "1.678" o "Q.E.P.D."
    punto = trozo.rfind(". ")
    if punto >= maximo * 0.45:
        return trozo[:punto + 1]
    espacio = trozo.rfind(" ")
    return trozo[:espacio].rstrip(" ,;:—–-“\"") + "…"


def seccion(n):
    c = [x for x in n["cats"] if x != "Destacadas"]
    c = c[0] if c else "Destacadas"
    return ROTULO.get(c, c)


def img(idx, eager=False):
    f = FOTO[idx]
    alt = esc(N[idx]["titulo"])
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="{f["src"]}" width="{f["w"]}" height="{f["h"]}" alt="{alt}" {load}>'


def nota(idx, cls="", bajada=False, volanta=True, eager=False, h="h3", largo=200):
    n = N[idx]
    v = f'<span class="volanta">{esc(seccion(n))}</span>' if volanta else ""
    texto = n.get("bajada_completa") or n["bajada"]
    b = f'<p class="bajada">{esc(corta(texto, largo))}</p>' if bajada and texto else ""
    return (f'<article class="nota {cls}">'
            f'<a class="nota__img" href="{n["link"]}">{img(idx, eager)}</a>'
            f'<div class="nota__txt">{v}<{h}><a href="{n["link"]}">{esc(n["titulo"])}</a></{h}>'
            f'{b}<p class="meta">{fecha(n["fecha"])}</p></div></article>')


def aviso(f, cls="aviso--h", rotulo=True):
    a = AV[f]
    r = '<span class="aviso__rot">Publicidad</span>' if rotulo else ""
    return (f'<aside class="aviso {cls}" aria-label="Publicidad">{r}'
            f'<a href="#" rel="sponsored noopener"><img src="{a["src"]}" width="{a["w"]}" '
            f'height="{a["h"]}" alt="Aviso" loading="lazy" decoding="async"></a></aside>')


def sec(titulo, slug, cuerpo):
    return (f'<section class="sec" aria-labelledby="s-{slug}">'
            f'<header class="sec__head"><h2 id="s-{slug}">{titulo}</h2>'
            f'<a class="sec__mas" href="https://elnuevocronista.com/category/{slug}/">Ver todo →</a></header>'
            f'{cuerpo}</section>')


def logo(borde="#1d1b1b"):
    """Redibujo vectorial del logo actual (logo.png 529x95), mismo diseno."""
    return f'''<svg viewBox="0 0 800 139" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="El Nuevo Cronista">
<defs><clipPath id="cl{borde[1:]}"><rect x="2" y="2" width="796" height="135" rx="11"/></clipPath></defs>
<g clip-path="url(#cl{borde[1:]})"><rect width="199" height="139" fill="#262424"/><rect x="199" width="601" height="139" fill="#E40204"/>
<path d="M199 96.5H800M199 103.5H800M199 110.5H800M199 117.5H800M199 124.5H800M199 131.5H800" stroke="#2A1414" stroke-width="2.4"/></g>
<rect x="2" y="2" width="796" height="135" rx="11" fill="none" stroke="{borde}" stroke-width="3"/>
<g font-family="Anton,Impact,sans-serif" fill="#fff" stroke="#1d1b1b" stroke-width="5" paint-order="stroke" stroke-linejoin="round">
<text x="28" y="123" font-size="119" textLength="136" lengthAdjust="spacingAndGlyphs">EL</text>
<text x="219" y="123" font-size="119" textLength="572" lengthAdjust="spacingAndGlyphs">CRONISTA</text>
<text transform="translate(193 122) rotate(-90)" font-size="29" stroke-width="2.6" textLength="104" lengthAdjust="spacingAndGlyphs">NUEVO</text>
</g></svg>'''


SOC = {
    "Facebook": '<path d="M13.5 21v-7.5h2.5l.4-3h-2.9V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H8v3h2.4V21z"/>',
    "Instagram": '<path d="M12 7.3A4.7 4.7 0 1 0 16.7 12 4.7 4.7 0 0 0 12 7.3m0 7.7a3 3 0 1 1 3-3 3 3 0 0 1-3 3m6-7.9a1.1 1.1 0 1 1-1.1-1.1A1.1 1.1 0 0 1 18 7.1M21.4 8a5.4 5.4 0 0 0-1.5-3.9A5.5 5.5 0 0 0 16 2.6c-1.5-.1-6.2-.1-7.8 0a5.5 5.5 0 0 0-3.9 1.5A5.4 5.4 0 0 0 2.6 8c-.1 1.5-.1 6.2 0 7.8a5.4 5.4 0 0 0 1.5 3.9A5.5 5.5 0 0 0 8 21.2c1.6.1 6.3.1 7.8 0a5.4 5.4 0 0 0 3.9-1.5 5.5 5.5 0 0 0 1.5-3.9c.1-1.6.1-6.3 0-7.8"/>',
    "WhatsApp": '<path d="M12 2.2A9.8 9.8 0 0 0 3.6 17l-1.4 5 5.2-1.4A9.8 9.8 0 1 0 12 2.2m0 17.9a8.1 8.1 0 0 1-4.1-1.1l-.3-.2-3.1.8.8-3-.2-.3A8.1 8.1 0 1 1 12 20.1m4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.3-.4.8-1.3a.5.5 0 0 0 0-.5c0-.1-.6-1.4-.8-1.9s-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.5 4 5.2 5.2 0 0 0 3.2.7 2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.2c0-.1-.2-.2-.4-.3"/>',
}
ICON_SOC = "".join(f'<a href="#" aria-label="{k}"><svg viewBox="0 0 24 24" aria-hidden="true">{v}</svg></a>'
                   for k, v in SOC.items())

MENU = [("Inicio", "", False), ("La Ciudad", "la-ciudad", False), ("Política", "politica", True),
        ("Seguridad", "policiales", False), ("Deportes", "deportes", False),
        ("Sociedad", "sociedad", False), ("Cultura", "cultura", False), ("Salud", "salud", False),
        ("Provinciales", "provinciales", False), ("Necrológicas", "necrologicas", False),
        ("Servicios", "servicios", False)]


def menu():
    out = []
    for t, slug, nuevo in MENU:
        href = f"https://elnuevocronista.com/{'category/' + slug + '/' if slug else ''}"
        cur = ' aria-current="page"' if not slug else ""
        cl = ' class="nuevo" title="Hoy no está en el menú: 1.288 notas"' if nuevo else ""
        out.append(f'<a href="{href}"{cur}{cl}>{t}</a>')
    return "".join(out)


def main():
    hoy = date(2026, 10, 12)
    fecha_larga = f"{DIAS[hoy.weekday()].capitalize()} {hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}"

    necros = [i for i, n in enumerate(N) if "Necrológicas" in n["cats"]]
    necro_html = "".join(
        f'<li><a href="{N[i]["link"]}"><span class="necro__cruz" aria-hidden="true">†</span>'
        f'{esc(N[i]["titulo"].replace(" Q.E.P.D.", ""))}</a><span>{fecha(N[i]["fecha"])} · Q.E.P.D.</span></li>'
        for i in necros)

    verticales = [f for f, a in AV.items() if a["forma"] == "vertical"]
    cuadrados = [f for f, a in AV.items() if a["forma"] == "cuadrado"]
    # horizontales en el orden de aparicion: cabecera, entre secciones y banda final
    H = ["banner-AEFIP.gif", "publi-tapa-web.jpg", "colegio-arquitectos-web.jpg", "cimes-banner.gif",
         "silvia-banner.gif", "vetrinaria-zubeldia.gif", "bomberos-banner-1.gif",
         "Carne.jpg", "bonetti_nov2020.jpeg", "zionnn.jpeg"]
    assert sorted(H) == sorted(f for f, a in AV.items() if a["forma"] == "horizontal"), "faltan horizontales"

    ciudad = (f'<div class="g-1l">{nota(34, "nota--gr", bajada=True, volanta=False)}'
              f'<div class="lista">{nota(30, volanta=False)}{nota(22, volanta=False)}{nota(56, volanta=False)}</div></div>')
    politica = f'<div class="g-2">{nota(28, bajada=True, volanta=False)}{nota(41, bajada=True, volanta=False)}{nota(31, volanta=False)}{nota(18, volanta=False)}</div>'
    # la destacada de deportes va en dos columnas: imagen | texto
    n26 = N[26]
    deportes = (f'<article class="nota dep-top"><a class="nota__img" href="{n26["link"]}">{img(26)}</a>'
                f'<div><span class="volanta">Patín adaptado</span><h3><a href="{n26["link"]}">{esc(n26["titulo"])}</a></h3>'
                f'<p class="bajada">{esc(corta(n26["bajada_completa"], 230))}</p><p class="meta">{fecha(n26["fecha"])}</p></div></article>'
                f'<div class="g-4">{nota(14, volanta=False)}{nota(8, volanta=False)}{nota(12, volanta=False)}{nota(10, volanta=False)}</div>')
    seguridad = f'<div class="g-1l">{nota(44, "nota--gr", bajada=True, volanta=False)}<div class="lista">{nota(0, volanta=False)}{nota(49, volanta=False)}{nota(19, volanta=False)}</div></div>'
    cultura = f'<div class="g-1l">{nota(29, "nota--gr", bajada=True, volanta=False)}<div class="lista">{nota(2, volanta=False)}{nota(13, volanta=False)}{nota(21, volanta=False)}</div></div>'
    sociedad = f'<div class="g-4">{nota(25, volanta=False)}{nota(24, volanta=False)}{nota(27, volanta=False)}{nota(55, volanta=False)}</div>'

    ticker = "".join(f'<a href="{N[i]["link"]}">{esc(N[i]["titulo"])}</a>' for i in (0, 36, 25))

    page = f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>El Nuevo Cronista — Propuesta de rediseño de portada</title>
<!-- maqueta privada: que Google no la indexe (seria contenido duplicado del diario real) -->
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="theme-color" content="#1A1A1C">
<link rel="preload" href="assets/fonts/Anton-latin-1Ptgg87LROyAm3Kz-C8.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="assets/css/cronista.css">
</head>
<body>

<div class="top"><div class="wrap">
  <span class="top__fecha">{fecha_larga} · Mercedes</span>
  <span class="top__ed">Edición impresa <b>Nº 1.678</b></span>
  <span class="top__soc">{ICON_SOC}</span>
</div></div>

<header class="masthead"><div class="wrap">
  <a class="masthead__logo" href="https://elnuevocronista.com/">{logo()}</a>
  <p class="masthead__lema">Semanario de Mercedes · Provincia de Buenos Aires</p>
</div></header>

<nav class="nav" aria-label="Secciones"><div class="wrap">
  <button class="nav__burger" aria-label="Abrir secciones" aria-expanded="false" aria-controls="menu">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
  <a class="nav__logo-mini" href="https://elnuevocronista.com/" aria-label="El Nuevo Cronista">{logo()}</a>
  <div class="nav__links" id="menu">{menu()}</div>
  <button class="nav__buscar" aria-label="Buscar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg></button>
</div></nav>

<div class="ticker"><div class="wrap">
  <span class="ticker__tag">Último momento</span>
  <div class="ticker__items">{ticker}</div>
</div></div>

<main class="wrap">

  {aviso(H[0])}

  <section class="apertura" aria-label="Lo más importante">
    <div class="lead">{nota(16, bajada=True, eager=True, h="h2", largo=300).replace('<span class="volanta">La Ciudad</span>', '<span class="volanta">Educación técnica</span>')}</div>
    <div class="apertura__col">{nota(4)}{nota(3, "nota--fila")}{nota(1, "nota--fila")}</div>
  </section>

  {aviso(H[1])}

  <div class="cuerpo">
    <div class="principal">
      {sec("La Ciudad", "la-ciudad", ciudad)}
      {sec("Política", "politica", politica)}
      {aviso(H[2])}
      {sec("Deportes", "deportes", deportes)}
      {aviso(H[3])}
      {sec("Seguridad", "policiales", seguridad)}
      {aviso(H[4])}
      {sec("Cultura", "cultura", cultura)}
      {aviso(H[5])}
      {sec("Sociedad", "sociedad", sociedad)}
    </div>

    <aside class="lateral" aria-label="Edición impresa, necrológicas y avisos">
      <section class="modulo impresa">
        <h2 class="modulo__t">Edición impresa</h2>
        <a class="impresa__tapa" href="#"><img src="assets/img/tapa-1678.webp" width="560" height="854" alt="Tapa de la edición impresa Nº 1.678" loading="lazy"></a>
        <p class="impresa__dato"><b>Nº 1.678</b> · 12 de octubre de 2026</p>
        <a class="btn" href="#">Ver la edición</a>
      </section>
      <section class="modulo">
        <h2 class="modulo__t">Necrológicas</h2>
        <ul class="necro">{necro_html}</ul>
        <a class="btn" href="https://elnuevocronista.com/category/necrologicas/">Ver todas</a>
      </section>
      <div class="lat-avisos">{"".join(aviso(f, "aviso--lat", rotulo=False) for f in verticales)}</div>
    </aside>
  </div>

  <section class="comercios" aria-labelledby="t-com">
    <div class="comercios__head"><h2 id="t-com">Comercios que nos acompañan</h2>
      <p>Gracias a ellos, El Nuevo Cronista llega a cada vecino.</p></div>
    <div class="comercios__grid">{"".join(f'<a href="#" rel="sponsored noopener" aria-label="Aviso"><img src="{AV[f]["src"]}" width="{AV[f]["w"]}" height="{AV[f]["h"]}" alt="Aviso" loading="lazy" decoding="async"></a>' for f in cuadrados)}</div>
  </section>

  {aviso(H[6])}{aviso(H[7], rotulo=False)}{aviso(H[8], rotulo=False)}{aviso(H[9], rotulo=False)}

</main>

<footer class="pie">
  <div class="wrap pie__top">
    <div>
      <div class="pie__logo">{logo("#5A5A60")}</div>
      <p class="pie__lema">Semanario de Mercedes · Provincia de Buenos Aires</p>
    </div>
    <div>
      <h4>El Nuevo Cronista</h4>
      <dl class="legal">
        <dt>Propietario</dt><dd>Javier Fernando Guevara</dd>
        <dt>Director responsable</dt><dd>Javier Fernando Guevara</dd>
        <dt>Domicilio legal</dt><dd>Calle 5 N° 619, Ciudad de Mercedes (B)</dd>
        <dt>Registro DNDA</dt><dd>En trámite</dd>
        <dt>Contacto</dt><dd><a href="mailto:info@elnuevocronista.com">info@elnuevocronista.com</a></dd>
      </dl>
    </div>
    <div>
      <h4>Secciones</h4>
      <ul class="pie__secs">{"".join(f'<li><a href="https://elnuevocronista.com/category/{s}/">{t}</a></li>' for t, s, _ in MENU if s)}</ul>
    </div>
  </div>
  <div class="pie__base"><div class="wrap">
    <span>© 2026 El Nuevo Cronista. Todos los derechos reservados.</span>
    <span>Mercedes, Buenos Aires</span>
  </div></div>
</footer>

<script>
(function(){{
  var b=document.querySelector('.nav__burger'), m=document.getElementById('menu');
  if(!b||!m) return;
  b.addEventListener('click',function(){{
    var a=b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded',String(!a)); m.classList.toggle('abierto',!a);
  }});
}})();
</script>
</body>
</html>
'''
    open(os.path.join(BASE, "index.html"), "w").write(page)
    usados = page.count('alt="Aviso"')
    print(f"index.html OK — avisos en la pagina: {usados} de {len(AV)}  "
          f"(H {len(H)} · V {len(verticales)} · C {len(cuadrados)})")
    print(f"notas en la pagina: {page.count('<article class=\"nota')} + {len(necros)} necrologicas")


if __name__ == "__main__":
    main()
