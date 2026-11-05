# Registro del LOOP

## Regla

Cada iteración declara objetivo, cambio, verificación y decisión. Un gate fallido
regresa a la etapa que produjo el defecto.

## Iteración 0. Congelar

**Objetivo:** fijar una GPC, CLRS capítulo 25 y la rúbrica.

**Decisiones:**

- fuente privada por hash;
- demo pública simbólica;
- una sola guía;
- exposición de 15 minutos.

**Gate:** fuente y teoría identificadas.

## Iteración 1. Corregir el constructo

**Problema detectado:** el planteamiento previo introducía un constructo ajeno
al propósito real de preparar generación sintética.

**Cambio:**

- U pasa a ser catálogo finito de estructuras de caso;
- V pasa a ser variantes clínicas de ruta;
- arista pasa a significar instanciabilidad ejecutable;
- salida pasa a ser assignment_manifest.json.

**Gate:** las particiones representan únicamente objetos pre-generativos.

## Iteración 2. Evitar circularidad

**Riesgo:** derivar una estructura de cada ruta y después declarar que son
compatibles.

**Cambio:**

- variantes desde \(D\);
- estructuras desde esquema y restricciones;
- compatibilidad evaluada solo después;
- canonical_signature ignora IDs.

**Gate:** los dos lados pueden construirse sin consultar el otro.

## Iteración 3. Definir ejecución

**Cambio:** \(\operatorname{Exec}_D\) se define como función parcial
determinista sobre el subgrafo XOR. Missingness insuficiente, contradicción o
múltiples ramas producen rechazo.

Cada arista persiste:

- witness_assignment;
- ruta observada;
- versión de reglas;
- fuente;
- código de decisión.

**Gate:** las catorce aristas tienen testigo.

## Iteración 4. Resolver

**Algoritmos:**

- baseline por caminos aumentantes;
- Hopcroft-Karp;
- oráculo independiente.

**Teoría:** Lema 25.1, Corolarios 25.2 y 25.4, Teorema 25.8 de CLRS.

**Resultado esperado:**

\[
|M^*|=7.
\]

**Gate:** cardinalidad concordante y matching válido.

## Iteración 5. Explicar el déficit

Para las ocho variantes, el vecindario contiene las siete estructuras:

\[
|S|=8>|N(S)|=7.
\]

Hall explica el déficit uno. No prioriza cuál variante debe quedar libre.

**Gate:** testigo reproducible y lenguaje no clínico-inferencial.

## Iteración 6. Producir el manifiesto

**Salida:** assignment_manifest.json con:

- hashes;
- pares;
- testigos;
- variantes libres;
- déficit;
- estados de validación.

El LOOP se detiene antes de generación narrativa o tabular.

**Gate:** unicidad y reproducibilidad.

## Iteración 7. Validación científica

Se separan:

1. algoritmo;
2. estructura;
3. contenido clínico;
4. generación futura.

**Gate:** ninguna capa hereda validez de otra.

## Iteración 8. Literatura

Se conectan:

- Peleg y GLIF3: GPC computables;
- Synthea: conocimiento y máquinas de estados para pacientes sintéticos;
- CPGPrompt: GPC a árboles ejecutables;
- Zhang y Zhou: evaluación multidimensional de datos sintéticos;
- CLRS y Hopcroft-Karp: asignación óptima.

**Gate:** novedad descrita como inferencia calibrada.

## Iteración 9. Rúbrica

| Criterio | Producto |
|---|---|
| teoría | notas y mapeo de CLRS |
| análisis | complejidad, Hall y límites |
| aplicación | etapa previa a síntesis |
| código | dos algoritmos y pruebas |
| Colab | demo reproducible |
| material | documentos y ficha |
| presentación | nueve diapositivas, 15 minutos |

## Estado final esperado

- algoritmo y topología KISS: verificados;
- reconstrucción clínica privada: auditable;
- panel clínico: pendiente;
- generación sintética: no iniciada;
- generalización: pendiente.

El LOOP conserva estos pendientes como parte del resultado científico.
