# Explicación de la pregunta KISS

## Pregunta recomendada

> **¿Cómo asignar, uno a uno, escenarios clínico-educativos simulados
> compatibles a microobjetivos de aprendizaje sobre severidad para maximizar el
> número de microobjetivos cubiertos, sin reutilizar casos?**

La versión inicial —“¿Cómo seleccionar el mayor número de casos...?”— podía
interpretarse como si el objetivo fuera contar casos. Eso sería trivial: si hay
siete, se seleccionan siete. La cantidad que realmente se optimiza es el número
de **pares caso-objetivo**, equivalente al número de objetivos que reciben un
representante distinto.

## Cada parte de la pregunta

### 1. “¿Cómo asignar...?”

No se busca una lista de casos ordenada por preferencia. Se busca una asignación:
un conjunto de pares `(caso, objetivo)` que cumplan reglas explícitas. En teoría
de grafos, esos pares son aristas seleccionadas.

### 2. “uno a uno”

Cada caso puede aparecer en, como máximo, un par y cada objetivo puede aparecer
en, como máximo, un par:

\[
\sum_v x_{uv}\leq 1\quad\forall u\in U,
\qquad
\sum_u x_{uv}\leq 1\quad\forall v\in V.
\]

Esta es la restricción que convierte el problema en matching bipartito.

### 3. “escenarios clínico-educativos simulados”

Son plantillas simbólicas derivadas de criterios estructurados de la GPC. No son
pacientes, historias clínicas completas ni datos sintéticos con una distribución
poblacional. Para el caso KISS se usa un escenario por cada uno de siete
criterios explícitos de severidad.

La palabra “caso” se conserva por su valor didáctico, pero el término técnico más
exacto es **escenario clínico-educativo simbólico**.

### 4. “compatibles”

Un caso y un objetivo son compatibles si el caso contiene los predicados y la
ruta estructural que la regla del objetivo exige, sin contradicciones y con
procedencia verificable. Una compatibilidad se dibuja como una arista.

La arista no afirma que el caso sea clínicamente seguro o realista. Afirma que la
regla computacional aprobó ese vínculo.

### 5. “microobjetivos de aprendizaje”

Un objetivo de aprendizaje completo suele expresar una conducta, una condición
y un nivel de desempeño. La GPC no entrega automáticamente esos objetivos
curriculares. Por eso, en este proyecto se definen **microobjetivos educativos
diseñados a partir de la guía**:

- `O1` a `O7`: identificar individualmente cada criterio de severidad en un
  escenario simulado;
- `O8`: reconocer la ruta/BPC asociada a la presencia de severidad.

Son unidades pequeñas y auditables. No se afirma que sean objetivos oficiales de
MINSA ni que cubran todo el currículo sobre preeclampsia.

### 6. “cubiertos”

En este proyecto, un objetivo está cubierto cuando recibe un caso compatible
como **representante principal** en el matching.

Por ejemplo, si se selecciona `(C3,O3)`, el caso `C3` acredita la presencia de un
representante para el microobjetivo `O3`. Eso no demuestra que un estudiante lo
haya aprendido. Solo demuestra cobertura estructural del banco de casos.

### 7. “objetivos distintos”

“Distintos” significa que son vértices deduplicados y cada uno se cuenta una
sola vez. No quiere decir necesariamente que pertenezcan a ocho dominios
cognitivos diferentes de Bloom.

La distinción evita inflar la cobertura contando repetidamente el mismo objetivo
con varios casos muy parecidos.

### 8. “sin reutilizar casos”

Cada caso se acredita a un solo objetivo principal. Esta regla puede representar:

- siete estaciones o fichas independientes;
- siete actividades asignadas a equipos diferentes;
- un banco donde se exige un ejemplo representativo distinto por objetivo;
- una evaluación donde no se desea que una sola viñeta cuente dos veces.

La regla no es una verdad pedagógica. Un caso real puede enseñar varias cosas. Es
una decisión de diseño para diversidad y ausencia de doble conteo.

## El grafo del ejemplo

Sea `U={C1,...,C7}` el conjunto de casos y
`V={O1,...,O7,O_BPC}` el conjunto de microobjetivos. Cada caso `Ci` tiene dos
aristas:

\[
(C_i,O_i)\quad\text{y}\quad(C_i,O_{BPC}).
\]

Por tanto:

\[
|U|=7,\qquad |V|=8,\qquad |E|=7+7=14.
\]

Existe un matching con siete pares, pero ningún matching puede tener ocho:

\[
|M|\leq\min(|U|,|V|)=7.
\]

Además, para el conjunto de los ocho objetivos, su vecindario contiene solo los
siete casos:

\[
|S|=8>|N(S)|=7.
\]

Es un testigo de Hall con déficit uno. Hopcroft-Karp construye una solución de
tamaño siete y la cota también es siete; por tanto, la solución es máxima.

## ¿Cuál objetivo queda fuera?

En un matching no ponderado puede quedar sin representante la BPC o cualquiera
de los siete criterios, según el desempate. La cardinalidad seguirá siendo siete.
El algoritmo no sabe cuál objetivo es clínicamente o pedagógicamente más
importante.

Si se necesita priorizar, habría que añadir pesos, prioridades o restricciones y
resolver una variante ponderada. Esa extensión es válida, pero se deja fuera de
la presentación KISS.

## La comparación epidemiológica útil

Este problema se parece a construir una base analítica solo en la disciplina de
las definiciones:

| Epidemiología | Proyecto KISS |
|---|---|
| unidad observacional | escenario simbólico |
| variable operacional | microobjetivo |
| criterio de elegibilidad | regla de compatibilidad |
| análisis | matching máximo |
| control de calidad | pruebas y procedencia |

No hay muestreo, estimando causal, intervalo de confianza ni validez externa
poblacional. El resultado `7` es determinista una vez fijado el grafo.

## Cuándo no usar matching

Si el propósito es que un mismo caso enseñe simultáneamente su criterio, la BPC,
diagnóstico y tratamiento, el matching uno-a-uno deja de representar la pregunta.
Según el objetivo, correspondería usar:

- *set cover* o máxima cobertura: un caso cubre varios objetivos;
- `b`-matching: un caso tiene capacidad mayor que uno;
- matching ponderado: algunas asignaciones valen más;
- flujo de costo mínimo: existen capacidades, cuotas y prioridades.

Esta frontera no debilita el proyecto. Define con precisión qué problema resuelve.

## Respuesta oral en veinte segundos

> Cubrir un objetivo significa asignarle un caso compatible como representante
> principal. Los objetivos son siete criterios de severidad y una ruta/BPC
> asociada. Como solo tenemos siete casos y no los reutilizamos, el matching
> máximo cubre siete de ocho. El grafo hace visible esa brecha; no mide aprendizaje
> ni validez clínica.
