# Auditoría semántica de flujogramas

## `flow_1` - prevención

- Inicio reconciliado: `n1`.
- Alcanzables: `n1,n2,n3,n4,n5,n6`.
- Terminales alcanzables: `n2,n5,n6`.
- Ciclos: ninguno.
- Aislados: ninguno.
- Semántica: `n1 --No--> n2` es una alternativa; las dos transiciones `Sí` hacia `n3` y `n4` forman una activación paralela `AND`; `n3->n5` y `n4->n6` son secuenciales.
- Gate: una firma positiva debe contener ambas ramas sin imponer un orden clínico inexistente.

## `flow_2` - manejo inicial

- Inicio reconciliado: `n2`.
- Alcanzables: `n1,n2,n3,n4,n5,n6,n7,n8`.
- Aislado: `n9`.
- Terminales clínico-estructurales alcanzables: `n1,n7,n8`.
- Ciclos: ninguno.
- Semántica: `n2` divide `Sí/No` como XOR; `n3->n4` es secuencial; `n4` divide `Sin criterios/Con criterios` como XOR.
- Gate: `n9` no puede originar ni completar una firma de ejecución.

## `flow_3` - método de evidencia

- Inicio reconciliado: `n1`.
- Alcanzables: los ocho nodos.
- Terminales: `n4,n7,n8`.
- Ciclos: ninguno.
- Alcance: no clínico; se excluye de `U`, `V` y `E`.

## Estados

| Riesgo | Estado | Efecto |
|---|---|---|
| Paralelismo `flow_1` | Validado por advertencia de fuente | Admitir firma AND |
| Terminal `flow_2:n9` | Rechazado como terminal clínico | Excluir de rutas |
| `route_templates` vacíos | Confirmado | Derivar firmas versionadas |
| `flow_3` | Fuera de alcance clínico | Solo auditoría |

