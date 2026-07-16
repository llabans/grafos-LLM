# Reconciliación entre flujogramas y Phase 4

## Método

Para cada `flow_id` se compararon identificadores de nodo, texto, tipo, endpoints y etiquetas. `flowcharts.json` se trató como fuente primaria; `decision_graphs.jsonl` se filtró por la guía objetivo y se trató como derivado.

## Resultado estructural

| Flujo | Nodos primario/derivado | Aristas primario/derivado | Cambios de texto o etiquetas | Resultado |
|---|---:|---:|---:|---|
| `flow_1` | 6/6 | 5/5 | 0 | Equivalente |
| `flow_2` | 9/9 | 7/7 | 0 | Equivalente |
| `flow_3` | 8/8 | 8/8 | 0 | Equivalente |

Phase 4 enriquece la representación con inicio, terminales, IDs de unidades y trazabilidad. No se integrará como un segundo conjunto de nodos o aristas.

## Diferencias semánticas que requieren control

- `flow_1`: la fuente primaria advierte que dos aristas `Sí` desde `n1` pueden ejecutarse simultáneamente. Se clasifica como `AND`.
- `flow_2`: el derivado incluye `n9` entre terminales por ausencia de salidas. La fuente primaria lo describe como nota aislada. Se conserva como información, pero se excluye de terminales alcanzables y firmas.
- Todos los `route_templates` están vacíos. Las firmas deben derivarse localmente y validarse.

## Política de resolución

Una diferencia de nodos, aristas o etiquetas bloquea la construcción de escenarios para ese flujo. Un enriquecimiento derivado solo se acepta si no contradice la fuente primaria y conserva procedencia.

