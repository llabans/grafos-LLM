# Auditoría de fuentes

## Alcance

La autoridad clínica está restringida a `gpc-05-hipertension-embarazo-2025`. El proyecto no incorpora pacientes, inferencias diagnósticas ni conocimiento médico externo.

## Conteos observados

| Artefacto | Conteo filtrado |
|---|---:|
| `recommendations.json` | 5 |
| `tables.json` | 221 |
| `flowcharts.json` | 3 |
| Segmentos Phase 4 | 30 |
| Unidades clínicas Phase 4 | 269 |
| Grafos Phase 4 | 3 |

Los conteos coinciden con el baseline del prompt. Los hashes completos están en `data/manifests/source_manifest.json`.

## Inventario funcional

- `flowcharts.json`: lista JSON de tres objetos con `id`, metadatos de página/sección, nodos, aristas y advertencias.
- `recommendations.json`: tres recomendaciones GRADE y dos BPC.
- `tables.json`: 221 tablas heterogéneas. `table_003`, páginas 9-11, contiene la estructura explícita de niveles de riesgo y enunciados principales.
- `structure.json`: metadatos documentales, 249 páginas declaradas y árbol de secciones.
- `bibliografia.json`: referencias de la propia guía; se usa solo como metadato.
- Phase 4: colecciones multiguía; todo acceso exige `source_id` exacto antes de contar o adaptar.

## Criterios de inclusión

1. El `source_id` coincide exactamente con la guía objetivo.
2. El elemento conserva identificador y página o sección cuando existe.
3. La estructura es explícita; una frase no se transforma automáticamente en predicado.
4. Una correspondencia entre fuentes requiere una regla de crosswalk declarada.
5. Toda ambigüedad se marca `human_review_required` o `blocked_by_evidence`.

## Exclusiones

- `outputs/pilot_30`: sandbox histórico no revalidado.
- `flow_3`: proceso metodológico de búsqueda/evaluación, no ruta clínica.
- `gpc-05-hipertension-embarazo-resumida-2025`: variante de 28 páginas excluida. Su relación con la guía canónica figura como `mapping_status=draft`; no se fusiona ni se usa para completar evidencia.
- `decision_graphs_filtered.jsonl`: sigue conteniendo múltiples guías y variantes; el nombre “filtered” no reemplaza el filtro exacto por `source_id`.
- Guías con cualquier otro `source_id`.
- Referencias bibliográficas no inspeccionadas como evidencia clínica.
- Tablas sin relación explícita con el caso demostrativo.

## Resultado

La fuente es suficiente para un caso educativo reproducible de cobertura algorítmica. No es suficiente para construir una herramienta clínica ni para completar relaciones ausentes mediante conocimiento externo.
