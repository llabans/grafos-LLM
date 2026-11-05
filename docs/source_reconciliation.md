# Reconciliación de fuente primaria y Phase 4

## Método

Para cada flow_id se comparan:

- IDs y tipos de nodo;
- texto normalizado;
- endpoints;
- etiquetas;
- entrada;
- terminales;
- procedencia.

**flowcharts.json** es la topología primaria. **decision_graphs.jsonl** es un
derivado y nunca se fusiona como un segundo grafo.

## Resultado

| Flujo | nodos primario/derivado | aristas primario/derivado | discrepancias textuales | decisión |
|---|---:|---:|---:|---|
| flow_1 | 6/6 | 5/5 | 0 | reconciliado; semántica AND |
| flow_2 | 9/9 | 7/7 | 0 | reconciliado; subgrafo XOR KISS |
| flow_3 | 8/8 | 8/8 | 0 | documental, fuera de alcance |

## Controles semánticos

- Las dos salidas positivas de flow_1 son paralelas, no XOR.
- El nodo aislado de flow_2 no se acepta como terminal por grado cero.
- Los route_templates derivados están vacíos; las variantes se enumeran
  localmente desde \(D\).
- Cada variante se deduplica por canonical_signature, no por ID.

## Política

Una diferencia de nodo, arista o etiqueta bloquea la reconstrucción. Un
enriquecimiento derivado solo se acepta si no contradice la fuente primaria.
Ningún conflicto se resuelve mediante un LLM.
