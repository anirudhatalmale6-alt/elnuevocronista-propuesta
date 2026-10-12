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

## Archivos

```
index.html                generado por tools/build_page.py
assets/css/cronista.css   estilos
assets/fonts/             Sofia Sans Condensed, Source Serif 4, Anton (autoalojadas)
assets/img/               imágenes en WebP al doble del tamaño en pantalla
tools/build_assets.py     baja y optimiza imágenes de notas y avisos
tools/build_page.py       arma la portada desde data/notas.json
```

`robots.txt` y `noindex`: la maqueta no debe aparecer en Google (sería
contenido duplicado del diario real).
