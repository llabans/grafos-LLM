# Auditoría de fuentes

## Alcance

La única autoridad clínica es el snapshot
**gpc-05-hipertension-embarazo-2025**. No se mezclan guías ni se completa
información con conocimiento externo.

## Inventario observado

| Artefacto | Conteo filtrado | Función |
|---|---:|---|
| recommendations.json | 5 | texto de recomendaciones y BPC |
| tables.json | 221 | criterios y valores estructurados |
| flowcharts.json | 3 | topología primaria |
| segmentos Phase 4 | 30 | unidades auxiliares |
| unidades clínicas Phase 4 | 269 | trazabilidad |
| grafos Phase 4 | 3 | representación derivada |

Los hashes se conservan en el manifiesto de fuente. Los conteos son controles de
drift, no constantes universales.

## Jerarquía de autoridad

1. **flowcharts.json:** nodos, aristas y etiquetas de transición.
2. **decision_graphs.jsonl:** representación derivada para reconciliar inicio,
   terminales e IDs.
3. **tables.json y recommendations.json:** predicados, criterios, acciones y
   texto fuente.
4. **structure.json:** páginas, secciones y contexto.
5. **Phase 4:** soporte de trazabilidad filtrado por source_id exacto.

Una similitud textual no crea un crosswalk.

## Inclusión

- source_id exacto;
- identificador reconstruible;
- página o sección cuando exista;
- estructura explícita;
- estado de revisión;
- hash de archivo.

## Exclusión

- cualquier otra guía;
- resumen de 28 páginas con mapping draft;
- outputs históricos no revalidados;
- flow_3 como trayectoria clínica;
- nodo informativo aislado de flow_2;
- tablas sin relación explícita con la demo;
- inferencias médicas no presentes en la fuente.

## IDs públicos

La demostración reemplaza identificadores y textos clínicos por símbolos
\(S_i\) y \(R_i\). Conserva topología y testigos abstractos. La auditoría clínica
completa solo puede ejecutarse con la fuente privada congelada.

## Resultado

La fuente es suficiente para una prueba pre-generativa y reproducible. No es,
por sí sola, evidencia de realismo de pacientes sintéticos ni autorización de
uso clínico.
