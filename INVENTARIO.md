# INVENTARIO — 3d

> Subinventario de este proyecto. Copia maestra en `silversun-dev/inventario` → `proyectos/3d.md`.
> **Estado: ✅ RELLENADO**

| Campo | Valor |
|---|---|
| Última actualización | 2026-09-22 |
| Actualizado por (sesión/rama) | sesión inventario (análisis inicial) — rama `claude/nice-johnson-y944m9` |
| Tipo de app | Otro: script de línea de comandos en Python 3 (solo biblioteca estándar), `analiza.py`, 105 líneas. No es una app publicable |
| **% listo para publicar** | 55 % (completitud para su propósito, no "publicación") |
| Justificación del % | Funciona: lee STL binario y ASCII y saca en JSON la ficha de cada modelo (gramos, horas, caja, piezas, encaje en bandeja, soporte, capas). Con un cubo de prueba de 20 mm los resultados son coherentes. Falta: se cae con STL vacíos, con STL binarios con bytes de más al final o con `volumen=0` (un solo archivo malo detiene todo el lote); el voladizo cuenta la cara apoyada en la cama; la estimación de horas no tiene en cuenta desplazamientos ni cambios de capa y queda muy por debajo de la real; no hay tests, README ni calibración contra un laminador real; no se puede comprobar que coincida con el "presupuestador original" porque no está en el repo |
| Destino previsto | Herramienta interna para precalcular las fichas del catálogo de productos impresos en 3D (la salida la usa otro sistema/catálogo que no está en este repo) |

## 1. Trabajo autónomo pendiente (lo que Claude puede hacer solo)
| # | Tarea | Tokens estimados |
|---|---|---|
| 1 | Robustez: capturar errores por archivo (seguir con el resto del lote), tratar STL vacío o con `volumen=0`, aceptar STL binarios con bytes de más al final, avisar si no se lee ningún triángulo | 40k |
| 2 | Tests automáticos con STL sintéticos (cubo, dos cuerpos, pieza con voladizo, ASCII, binario con cabecera "solid") | 50k |
| 3 | README con uso, significado de cada campo de la ficha y ejemplo de salida | 20k |
| 4 | Corregir el voladizo: excluir las caras apoyadas en la cama; detectar mallas abiertas o con normales invertidas y avisar (hoy `abs(vol)` lo oculta y el voladizo sale mal) | 80k |
| 5 | CLI: `argparse`, procesar una carpeta entera, escribir `fichas.json`, perfil de máquina en JSON en lugar de constantes en el código | 50k |
| 6 | Estimación de tiempo más realista (factor de desplazamientos y de capas, calibrable con los datos del usuario) | 80k |
| 7 | Rendimiento con STL grandes (cientos de miles de triángulos): optimizar bucles o usar numpy si es opcional | 80k |
| 8 | (Si se decide) cálculo de precio en la ficha (€/g, €/h, margen) | 50k |
| | **TOTAL** | **450k** |

## 2. Decisiones pendientes (las toma el usuario)
- [ ] ¿Dónde está el "presupuestador original" y el catálogo que consume estas fichas? ¿Se trae a este repo para comprobar que las fórmulas coinciden?
- [ ] Parámetros reales de la máquina y del material: bandeja 180×180×180 mm, caudal 5 mm³/s, densidad 1,24 (PLA), relleno 18 %, 2 perímetros, línea 0,42 mm, capa 0,2 mm. ¿Son los de tu impresora y material?
- [ ] ¿La ficha debe incluir el precio o el precio se calcula en el catálogo?
- [ ] ¿Se permite depender de numpy (más rápido) o se sigue solo con la biblioteca estándar?
- [ ] Formato de salida: JSON por pantalla (como ahora), archivo `fichas.json` o CSV
- [ ] ¿Se renombra la rama por defecto `claude/nice-johnson-y944m9` a `main`?

## 3. Pruebas manuales que tiene que hacer el usuario
- [ ] Pasar varios STL reales del catálogo y comparar gramos y horas con lo que da tu laminador (Cura/PrusaSlicer/Bambu) y con el peso real en báscula
- [ ] Comparar los resultados con los precios o fichas del presupuestador original
- [ ] Probar STL exportados desde tus programas habituales (ASCII y binario) y alguno grande para ver cuánto tarda
- [ ] Comprobar que el campo `encaje` ("ok" / "girado" / "no") cuadra con tu bandeja real

## 4. Cómo probar la app
- Enlace / acceso directo: no hay (ni web, ni releases, ni workflows). Es un script local
- Instrucciones: `python3 analiza.py modelo1.stl modelo2.stl > fichas.json` (Python 3, sin dependencias). Los `*.stl` y `fichas.json` están en `.gitignore`, así que el repo no trae modelos de ejemplo

## 5. Peligros, problemas y avisos
- ⚠️ **Un solo STL malo detiene todo el lote**: con un archivo vacío, con `volumen=0` o con un STL binario con bytes de más al final (el script lo trata como ASCII, no lee ningún triángulo) da `ZeroDivisionError` y no sale ninguna ficha. Comprobado
- ⚠️ **La estimación de horas queda muy por debajo de la real**: solo divide el volumen extruido entre el caudal y no cuenta desplazamientos, cambios de capa ni calentamiento. Un cubo de 20 mm sale en 0,17 h (unos 10 min). Si los precios dependen de las horas, se venderá por debajo del coste
- ⚠️ El voladizo (`voladizo_cm2`) cuenta la cara apoyada en la cama (el cubo de prueba da 4 cm² de voladizo). El soporte en gramos no se ve afectado porque esa cara está a altura 0
- ⚠️ Supone mallas cerradas y bien orientadas: con normales invertidas, `abs(vol)` oculta el error pero voladizo y soporte salen mal. Las cavidades internas cuentan como "piezas" separadas
- ⚠️ `encaje` = "girado" solo prueba intercambiar ejes; no vuelve a calcular soporte ni tiempo con la pieza en esa orientación
- ⚠️ No se puede comprobar que coincida con el "presupuestador original" (no está en el repo) y las constantes de máquina y material son valores fijos sin documentar
- ⚠️ Sin tests, sin README, sin datos de ejemplo; solo 2 commits y la rama por defecto es `claude/nice-johnson-y944m9`, no `main`

## 6. Historial de sesiones
| Fecha | Qué se hizo | % tras la sesión |
|---|---|---|
| 2026-09-22 | Creada plantilla vacía de inventario | — |
| 2026-09-22 | Análisis inicial y relleno del inventario | 55% |
