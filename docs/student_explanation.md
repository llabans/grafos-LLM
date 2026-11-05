# Explicación para una estudiante de maestría en ingeniería estadística

## Punto de partida desde medicina y epidemiología

Piensa en este proyecto como una cadena de **definición operacional → control de datos → optimización → validación**. Ese flujo es familiar en epidemiología: antes de estimar una asociación se define la población, exposición, desenlace y reglas de inclusión. Aquí no estimamos una asociación; definimos dos conjuntos de objetos y preguntamos cuántas asignaciones uno-a-uno pueden hacerse sin violar compatibilidad.

La semejanza útil está en la disciplina de diseño. La diferencia crucial está en el objeto:

| En epidemiología | En este proyecto |
|---|---|
| personas/unidades observacionales | escenarios simbólicos generados por reglas |
| variable de desenlace | obligación estructural de cobertura |
| criterio de elegibilidad | predicados y acciones requeridos |
| diccionario de datos | dataclasses y contratos de adaptador |
| diagrama causal o flujo clínico | grafo dirigido `D` |
| asignación combinatoria | grafo bipartito `B` y matching |
| auditoría de linaje | `SourceReference` + SHA-256 |

No son equivalentes, pero el paralelo ayuda a ubicar cada responsabilidad.

## La confusión más probable: “matching” no significa propensity-score matching

En epidemiología, *matching* suele seleccionar sujetos comparables para controlar confusión. Se habla de distancia, caliper, balance de covariables y estimandos causales. Nada de eso ocurre aquí.

En teoría de grafos, un matching es un subconjunto de aristas que no comparte endpoints. Si `u` representa un escenario y `v` un objetivo, elegir `(u,v)` consume ambos: ese escenario y ese objetivo no pueden aparecer en otro par.

Por tanto:

- no hay tratamiento ni control;
- no se estima propensity score;
- no se pretende intercambiabilidad;
- no se calcula efecto causal;
- no existen pacientes reales o sintéticos;
- la palabra “máximo” se refiere a cardinalidad, no a beneficio clínico.

## Dos grafos y por qué necesitamos ambos

### Grafo dirigido `D=(N,A)`

Es el equivalente a preservar el diagrama de proceso original. Las flechas tienen dirección y pueden expresar alternativas o secuencias. Sirve para responder:

- ¿qué nodo inicia el flujo?;
- ¿qué nodos son alcanzables?;
- ¿cuáles son terminales alcanzables?;
- ¿una bifurcación es `AND`, `XOR` o ambigua?;
- ¿existe un nodo aislado?

No se aplica Hopcroft–Karp sobre este grafo.

### Grafo bipartito `B=(U,V,E_B)`

Aquí las aristas no significan “sigue clínicamente a”. Significan “este escenario satisface esta obligación bajo la regla documentada”.

- `U`: 75 escenarios simbólicos.
- `V`: 35 obligaciones.
- `E_B`: 267 compatibilidades demostradas.

La bipartición es una restricción de tipos: no existe arista escenario–escenario ni objetivo–objetivo.

## Del dato crudo al objeto estadístico-computacional

La transformación se parece a preparar un dataset analítico:

1. **Congelar la fuente.** Los hashes cumplen una función análoga a versionar la base exacta usada en un análisis.
2. **Validar contratos.** Tipos, IDs y endpoints deben existir.
3. **Reconciliar representaciones.** Se compara el flujograma primario con Phase 4 para no contar el mismo fenómeno dos veces.
4. **Definir variables operacionales.** Los textos explícitos se normalizan a predicados con reglas auditables.
5. **Generar unidades.** Los escenarios se producen por combinatoria declarada, no por narración libre.
6. **Definir objetivos.** Se deduplican por concepto e ID.
7. **Construir relaciones.** Cada par candidato se aprueba o rechaza con explicación.
8. **Optimizar.** El solver opera únicamente sobre IDs y adyacencia.

La regla “primero diseño, luego cálculo” es tan importante aquí como en un protocolo epidemiológico.

## De dónde salen los 75 escenarios

La aritmética es completamente reproducible:

\[
10 + \binom{11}{2} + 1 + 1 + 1 + 7
=10+55+1+1+1+7=75.
\]

- 10 escenarios usan individualmente cada factor de riesgo alto explícito.
- 55 representan todos los pares no ordenados de 11 factores moderados.
- 1 representa el perfil leve explícito.
- 2 representan ramas estructurales de `flow_2` sin criterio de severidad.
- 7 usan individualmente cada criterio de severidad explícito.

No hay una “muestra” de 75 pacientes. Es el universo finito generado por esas reglas.

## De dónde salen los 35 objetivos

\[
35=10+11+7+5+2.
\]

Son 10 factores altos, 11 moderados, 7 criterios de severidad, 5 recomendaciones/BPC y 2 resultados estructurales. El objetivo es cubrir tantos como sea posible con representantes distintos.

## Qué significa una arista

Supón que un objetivo requiere predicado `p` y acción `a`. Un escenario es compatible si:

1. contiene todos los predicados requeridos;
2. no contiene un predicado prohibido;
3. activa todas las acciones esperadas;
4. escenario y objetivo están validados;
5. ambos pertenecen a la guía autorizada;
6. existe procedencia verificable.

Esto se parece a una regla de inclusión multivariable, pero no genera una probabilidad. La salida es binaria y determinista.

Una ausencia de arista se lee:

> “No se demostró compatibilidad bajo esta versión de reglas y esta fuente”.

No se lee “la conducta es incorrecta” ni “el caso no debe tratarse”.

## Matching maximal, máximo y perfecto

- **Maximal:** no puedes agregar una arista sin romper unicidad. Puede ser subóptimo.
- **Máximo:** tiene la mayor cardinalidad global.
- **Perfecto:** cubre todos los vértices de ambos lados; exige tamaños compatibles y suficiente conectividad.

La analogía estadística sería distinguir un algoritmo que llegó a un punto donde no sabe mejorar de una solución certificada como óptima. “No puedo añadir localmente” no implica “alcancé el máximo global”.

## Camino aumentante paso a paso

Considera:

- escenarios `u1,u2`;
- objetivos `v1,v2`;
- aristas `u1-v1`, `u1-v2`, `u2-v1`;
- matching actual `M={u1-v1}`.

`u2` está libre. No puede tomar `v1` directamente porque está ocupado. Pero existe el camino:

\[
u2 - v1 - u1 - v2.
\]

Las aristas alternan “fuera, dentro, fuera” del matching. Al invertir su estado:

\[
M'={u2-v1,u1-v2},
\]

y la cardinalidad pasa de 1 a 2. La reasignación es la idea esencial del DFS aumentante y de Hopcroft–Karp.

## Qué añade Hopcroft–Karp

El baseline encuentra un camino por vez. Hopcroft–Karp usa BFS para identificar la longitud mínima de los aumentos disponibles y DFS para encontrar varios caminos disjuntos de esa longitud en una misma fase.

Desde ingeniería estadística, puedes verlo como evitar trabajo redundante: BFS construye una estructura de admisibilidad global y DFS explota esa estructura antes de recalcularla.

Con `n` vértices totales y `m` aristas:

- DFS basal: `O(nm)` como cota general;
- Hopcroft–Karp: `O(m√n)` sobre el grafo activo;
- espacio de ambas implementaciones: `O(n+m)`.

Como el software conserva aislados, el costo completo de Hopcroft–Karp se documenta como `O(n+m√n)`.

## Por qué el resultado es 33 y no 35

Hay dos razones distintas.

### 1. Brecha de evidencia

El objetivo asociado a `rec_3` tiene grado cero. Ningún escenario demuestra simultáneamente los requisitos y una acción explícita reconciliada. Formalmente:

\[
|S|=1,\quad |N(S)|=0.
\]

### 2. Cuello de capacidad

Siete escenarios de severidad deben representar ocho objetivos: siete criterios individuales y una BPC asociada. Cada escenario puede usarse una vez:

\[
|S|=8,\quad |N(S)|=7.
\]

Por la condición de Hall, al menos uno de esos ocho objetivos quedará libre. Esto no es falta de una arista individual; es competencia colectiva por capacidad.

Los dos déficits suman 2. Como hay 35 objetivos:

\[
|M|\le35-2=33.
\]

El algoritmo encuentra 33, así que la solución alcanza la cota superior y es óptima.

## Cómo interpretar 94,3 %

\[
\frac{33}{35}\times100=94,2857\%.
\]

Es **cobertura combinatoria uno-a-uno**. No es:

- accuracy;
- sensibilidad o especificidad;
- valor predictivo;
- proporción de pacientes cubiertos;
- adherencia a la guía;
- calidad de atención.

El denominador son obligaciones construidas, no individuos.

## Lectura de los benchmarks

En el demo pequeño, DFS y Hopcroft–Karp tardan alrededor de 0,15 ms. No hay base para afirmar una superioridad temporal práctica con ese único grafo.

En el fixture escalera de 512 vértices por lado:

- DFS: 262.144 escaneos y mediana ≈37,98 ms;
- Hopcroft–Karp: 2.046 escaneos y mediana ≈0,55 ms.

El fixture está construido para revelar la revisita cuadrática del baseline. Es equivalente a usar un caso de simulación con mecanismo conocido para comprobar que un estimador o algoritmo responde como predice la teoría. No describe la distribución de grafos clínicos.

## ¿Dónde está la “estadística” en este proyecto?

El núcleo es algorítmico, pero la ingeniería estadística aparece en:

- especificación del objeto medido;
- calidad, linaje y versionado de datos;
- prevención de leakage entre fuentes;
- diseño de reglas reproducibles;
- separación entre resultados deterministas y evidencia empírica;
- resumen robusto de tiempos con mediana y cuartiles;
- análisis de validez interna, de constructo y externa;
- rechazo de inferencias no sustentadas.

Una buena defensa académica no necesita “forzar” una prueba estadística. Reconocer que los tiempos repetidos no constituyen una muestra inferencial es una decisión metodológica correcta.

## Cómo leer el código

Orden recomendado:

1. `domain/`: vocabulario y contratos.
2. `ingestion/`: cómo se fija y filtra la fuente.
3. `validation/source_reconciliation.py`: cómo se protege la semántica de `D`.
4. `integration/scenario_generator.py`: por qué `|U|=75`.
5. `integration/coverage_target_builder.py`: por qué `|V|=35`.
6. `integration/compatibility_builder.py`: por qué existe cada arista.
7. `matching/augmenting_path.py`: baseline.
8. `matching/hopcroft_karp.py`: algoritmo principal.
9. `matching/analysis.py`: testigos de Hall.
10. `tests/`: evidencia observable de cada invariante.

## Preguntas de defensa oral

### “¿Por qué no usar set cover?”

Porque el objetivo curricular exige una asignación uno-a-uno. *Set cover* permitiría que un escenario cubriera simultáneamente muchos objetivos y buscaría minimizar cuántos escenarios usar; es otro problema.

### “¿Por qué NetworkX si implementaste el algoritmo?”

Como oráculo independiente. El demo ejecuta código propio; NetworkX verifica cardinalidad en pruebas y no reemplaza la implementación.

### “¿Por qué no completar `rec_3` con conocimiento médico?”

Porque eso rompería el gate de fuente. La ausencia es un resultado de auditoría, no un hueco que deba maquillarse.

### “¿Por qué la BPC compite con criterios de severidad?”

Porque matching consume un escenario por objetivo. Ese cuello muestra la diferencia entre compatibilidad múltiple y selección uno-a-uno.

### “¿Qué prueba que 33 es máximo?”

Tres capas: criterio de caminos aumentantes, concordancia entre solvers/oráculos y cota superior constructiva mediante dos testigos de Hall.

### “¿Cuál es la principal amenaza a la validez?”

La definición de compatibilidad: aunque su implementación sea exacta, una regla alternativa produciría otro grafo. Por eso está versionada, explicada y limitada al propósito educativo.

## Mensaje final para la presentación

El valor del proyecto no es que “un algoritmo leyó medicina”. Es que una cadena auditable transformó una fuente estructurada en un problema matemático bien definido, demostró el óptimo, explicó sus brechas y evitó inferencias clínicas indebidas.
