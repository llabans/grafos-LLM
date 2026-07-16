# Validación KISS

## Qué sí está demostrado

- \(B\) es bipartito y tiene topología \(7-8-14\).
- Cada estructura tiene dos compatibilidades preespecificadas.
- Existe un matching de siete pares.
- No puede existir uno de ocho porque \(|U|=7\).
- Hall localiza un déficit de uno: \(8>7\).
- Baseline y Hopcroft-Karp resuelven el mismo problema.

## Qué significa

Siete variantes pueden reservar entradas independientes del catálogo en
**assignment_manifest.json**. Una de las ocho variantes queda sin estructura
reservada bajo capacidad unitaria.

## Qué no significa

- que se hayan generado siete pacientes;
- que una variante sea clínicamente menos importante;
- que la GPC quede validada;
- que los futuros datos sean realistas o privados;
- que \(7/8\) sea una medida epidemiológica.

## Cuatro capas

| Capa | Evidencia |
|---|---|
| algorítmica | pruebas, oráculo, camino aumentante, cota |
| estructural | rutas, testigos, aristas y Hall |
| clínica | especialistas y trazabilidad a la GPC |
| generativa | fidelidad, consistencia, diversidad, utilidad y privacidad |

## Lenguaje científico

La formulación correcta es:

> Prueba de concepto de una capa combinatoria previa a la generación sintética,
> fundamentada en GPC computables y matching bipartito.

No se afirma prioridad mundial ni validación clínica completa.

## Decisión siguiente

El resultado ofrece tres opciones explícitas:

1. añadir una octava estructura independiente;
2. aceptar que una variante no se incluya en el primer manifiesto;
3. permitir reutilización y cambiar el problema a set cover o capacidades
   mayores.

La elección es clínica y de diseño; el matching solo expone la restricción.
