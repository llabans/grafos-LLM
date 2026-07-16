# Siete estructuras, ocho variantes

## Pregunta

¿Cuántas variantes clínicas de una GPC pueden reservar una estructura de caso
independiente antes de generar datos sintéticos?

## Modelo

| Partición | Contenido | Tamaño |
|---|---|---:|
| \(U\) | catálogo piloto de estructuras | 7 |
| \(V\) | variantes clínicas de ruta | 8 |
| \(E\) | compatibilidades con testigo | 14 |

\[
(u,v)\in E
\iff
\exists x\in\operatorname{Inst}(u):
\operatorname{Exec}_D(x)=v.
\]

## Resultado

\[
|M^*|=7.
\]

- existe un matching de siete;
- no puede existir uno mayor que \(|U|\);
- Hall: \(8>7\), déficit uno.

## Semántica

Siete variantes incluyen un criterio de severidad focal. La octava no tiene
severidad. Cada estructura puede instanciar su variante focal o la variante
común con los siete criterios ausentes.

## Producto

**assignment_manifest.json** contiene pares, testigos, hashes, variante libre y
estado de validación.

## Base

- CLRS, cuarta edición, capítulo 25;
- Hopcroft y Karp, 1973;
- Peleg et al., 2003;
- GLIF3, 2004;
- Synthea, 2018;
- CPGPrompt, 2026.

## Límites

Se validan algoritmo y topología. La fidelidad clínica requiere panel. La
fidelidad, diversidad, utilidad y privacidad sintéticas se evalúan después de
generar.
