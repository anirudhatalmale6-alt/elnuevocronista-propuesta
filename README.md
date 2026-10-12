# El Nuevo Cronista — propuesta de portada

Maqueta de rediseño de la portada de **elnuevocronista.com** (Semanario de
Mercedes, Provincia de Buenos Aires). Es una propuesta visual: no reemplaza al
sitio ni toca el WordPress en vivo.

**Todo el contenido es real**: las 29 notas, las 6 necrológicas, la tapa de la
edición impresa Nº 1.678 y los 31 avisos salen del sitio actual (API pública de
WordPress, semana del 4 al 12 de octubre de 2026). No se inventó ningún título.

## Qué cambia

- Identidad del diario de papel en la web: volantas en rojo, titulares
  condensados, filetes entre secciones, colores del logo.
- Logo redibujado en vectorial (mismo diseño; el actual es un PNG de 529 px).
- "Política" en el menú (1.288 notas, hoy no figura).
- Módulos de Edición impresa y Necrológicas.
- Los 31 avisos ordenados por forma: horizontales entre secciones, verticales
  en el lateral, cuadrados en "Comercios que nos acompañan".
- Pie con los datos legales legibles y sin el "Buy now!" del tema.

## Medido en celular (390 px)

| | Hoy | Propuesta |
|---|---|---|
| Espacio que ocupan los mismos 31 avisos | 8.294 px (≈10 pantallas) | 3.149 px (≈4 pantallas) |
| Notas en la portada | 65 | 36 |

La portada de hoy muestra más notas: **la comparación justa es la de los avisos**,
no el largo total de la página.

## Versión 2: más noticias por sección (`mas-noticias.html`)

Pedido de Javier: "que en cada sección se vean más noticias". Cada sección
muestra 10 notas (Deportes 12) con este orden: 1 destacada, 3 con miniatura,
4 en grilla y titulares sin foto. Se suman Salud y Provinciales. Las notas salen
de las últimas 14 de cada categoría (`data/secciones.json`).

| Medido en celular (390 px), mismo método en las tres | Hoy | V1 | V2 |
|---|---|---|---|
| Notas en la portada | 65 | 36 | 84 |
| Alto de la página | 23.768 px | 13.309 px | 18.555 px |
| Espacio de los 31 avisos | 8.294 px | 3.143 px | 3.143 px |
| Peso | 8,15 MB | 3,29 MB | 3,43 MB |

La V2 muestra **más notas que hoy, en una página más corta y con menos de la
mitad del peso**, con los mismos 31 avisos.

## Archivos

```
index.html                generado por tools/build_page.py
assets/css/cronista.css   estilos
assets/fonts/             Sofia Sans Condensed, Source Serif 4, Anton (autoalojadas)
assets/img/               imágenes en WebP al doble del tamaño en pantalla
tools/build_assets.py     baja y optimiza imágenes de notas y avisos
tools/build_page.py       arma la portada (v1) desde data/notas.json; armar() es comun a las dos
tools/build_page_v2.py    v2: mas notas por seccion, desde data/secciones.json
```

`robots.txt` y `noindex`: la maqueta no debe aparecer en Google (sería
contenido duplicado del diario real).
