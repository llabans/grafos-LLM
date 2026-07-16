# Arquitectura del pipeline

```text
adaptadores de fuente
        |
        v
modelos canónicos tipados
        |
        v
validación + reconciliación
        |
        v
firmas + criterios + crosswalk
        |
        v
escenarios U + objetivos V
        |
        v
compatibilidad explicable E
        |
        v
solver puro + métricas + evidencia
```

## Separación de responsabilidades

- Los adaptadores conocen formatos, no matching.
- Los validadores conocen contratos, alcance y procedencia.
- Las etapas de integración conocen reglas explícitas versionadas.
- El constructor de compatibilidad es puro y determinista.
- Los solvers conocen solo conjuntos y adyacencia.
- Los reportes separan resultados clínico-estructurales, fixtures matemáticos y expectativas teóricas.

## Gates

Cada etapa rechaza entrada inválida. Un conflicto de fuente no se convierte en advertencia silenciosa; impide que el elemento llegue a `E`.

