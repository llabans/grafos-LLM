# Siete casos, ocho objetivos

## Pregunta

¿Cómo asignar casos clínico-educativos simulados compatibles a microobjetivos
distintos, uno a uno, para maximizar la cobertura sin reutilizar casos?

## Modelo

| Partición | Contenido | Tamaño |
|---|---|---:|
| `U` | escenarios de severidad | 7 |
| `V` | 7 criterios + 1 ruta/BPC | 8 |
| `E` | criterio propio + BPC por caso | 14 |

Un matching no comparte casos ni objetivos.

## Resultado y certificado

```text
|M*| = 7             cobertura estructural = 7/8 = 87,5 %
Hall: |S|=8 > |N(S)|=7                 déficit = 1
```

Siete pares son factibles y no puede haber ocho porque solo existen siete casos.

## Decisión de diseño

1. añadir un caso compatible e independiente; o
2. permitir cobertura múltiple y cambiar a otro modelo.

## Qué significa “cubrir”

Asignar un caso como representante principal del objetivo. No demuestra
aprendizaje, realismo clínico ni beneficio en pacientes.

## Base

- Cormen et al., *Introduction to Algorithms*, 4.ª ed., capítulo 25.
- Hopcroft y Karp (1973), DOI `10.1137/0202019`.
- Kandula y Bhattacharyya (2023), arXiv `2308.02984`.
- Gupta et al. (2025), arXiv `2501.13984`.
- Hicke et al., MedSimAI (2025/2026), arXiv `2503.05793`.

## Estado

Algoritmo validado; propuesta científicamente fundamentada; validación experta
del contenido y evaluación educativa pendientes.
