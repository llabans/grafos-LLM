# Formulación del problema

## Pregunta

> ¿Cuál es el mayor número de variantes clínicas de ruta derivadas de una GPC que
> puede recibir una estructura de caso distinta, trazable y todavía no narrada,
> sin reutilizar estructuras?

## Tres objetos que no deben confundirse

1. **Estructura de caso clínico:** variables, dominios, restricciones,
   missingness y procedencia; todavía puede admitir varias realizaciones.
2. **Instancia de caso clínico:** asignación concreta de valores que determina
   una trayectoria.
3. **Caso o registro sintético final:** realización narrativa o tabular de la
   instancia, potencialmente acompañada de metadatos y eventos longitudinales.

El proyecto opera en el primer nivel y entrega instrucciones para pasar al
segundo.

## Entradas

- Una única GPC oficial fijada por versión y hash.
- Un grafo dirigido de decisión \(D=(N,A)\).
- Un catálogo finito \(U\) de estructuras de caso clínico para un lote piloto,
  con capacidad unitaria explícita.
- Un conjunto \(V\) de variantes clínicas de ruta completas, canónicas y
  alcanzables, representadas por **ClinicalRouteVariant**.
- Un ejecutor parcial y determinista que evalúa instancias sobre un subgrafo de
  decisiones XOR de \(D\).

## Regla de arista

Para \(u\in U\) y \(v\in V\):

\[
(u,v)\in E
\iff
\exists x\in\operatorname{Inst}(u):
\operatorname{Exec}_D(x)=v.
\]

La función \(\operatorname{Exec}_D\) es parcial: devuelve rechazo ante datos
insuficientes, contradicción o rama no determinable. En cada nodo XOR, una
instancia válida habilita exactamente un sucesor.

La existencia debe acompañarse de un **witness_assignment persistido**: una asignación
concreta \(x\) que satisface los predicados requeridos, excluye los prohibidos y
alcanza el terminal declarado. Una similitud textual o la opinión libre de un
LLM no crea una arista.

## Problema de optimización

Sea \(x_{uv}\in\{0,1\}\) para cada \((u,v)\in E\). Se resuelve:

\[
\max \sum_{(u,v)\in E}x_{uv}
\]

sujeto a:

\[
\sum_{v:(u,v)\in E}x_{uv}\leq1
\qquad \forall u\in U,
\]

\[
\sum_{u:(u,v)\in E}x_{uv}\leq1
\qquad \forall v\in V.
\]

La solución induce \(M=\{(u,v):x_{uv}=1\}\).

## Instancia KISS

- \(U=\{S_1,\ldots,S_7\}\): siete estructuras simbólicas;
- \(V=\{R_1,\ldots,R_7,R_0\}\): siete rutas con criterio de severidad
  focal y una ruta sin severidad;
- \(E=\{(S_i,R_i),(S_i,R_0):1\leq i\leq7\}\).

Las variantes se derivan primero de \(D\) y se deduplican mediante una
**canonical_signature** que ignora el ID. Las estructuras se construyen por una
vía independiente desde el esquema de variables y restricciones; no se copian
de \(V\). Esta separación evita una compatibilidad circular.

Cada \(S_i\) contiene los siete indicadores de severidad. Puede generar un
testigo con el criterio \(i\) presente y los demás controlados para \(R_i\), o
un testigo con los siete ausentes para \(R_0\).

Por tanto:

\[
|U|=7,\quad |V|=8,\quad |E|=14,\quad |M^*|=7.
\]

## Optimalidad y déficit

Un matching de siete pares es una cota inferior constructiva. La cardinalidad de
\(U\) es una cota superior de siete. Ambas coinciden.

Para \(S=V\), \(N(S)=U\), de modo que:

\[
|S|-|N(S)|=8-7=1.
\]

Hall prueba que no existe asignación que cubra las ocho rutas con estructuras
distintas. La brecha describe capacidad de representación, no prevalencia,
riesgo ni importancia clínica.

## Hipótesis y criterios de refutación

**Hipótesis H1.** El algoritmo devuelve la cardinalidad óptima para todo grafo de
compatibilidad válido.

Se refuta si difiere del óptimo por enumeración exhaustiva en grafos pequeños o
de un solver independiente.

**Hipótesis H2.** Cada arista publicada posee al menos un testigo que ejecuta
exactamente la ruta declarada.

Se refuta si el testigo viola una restricción, alcanza otra ruta o no puede
reproducirse.

**Hipótesis H3.** El matching produce **assignment_manifest.json** sin reutilizar
estructuras ni rutas.

Se refuta si un identificador aparece en más de un par seleccionado.

## Salida

El producto no es un conjunto de pacientes. Es **assignment_manifest.json** con:

- identificador y versión de la GPC;
- hash del grafo dirigido y de las reglas;
- pares estructura-ruta seleccionados;
- witness_assignment persistido por par;
- rutas no asignadas y motivo;
- semilla y versión del algoritmo;
- estado de validación por capa.

## Por qué matching y no set cover

Matching responde cuántas rutas pueden reservar una estructura independiente.
Set cover respondería cuál es el menor conjunto de estructuras que, permitiendo
reutilización, puede instanciar todas las rutas. Esa es una extensión posterior,
no el problema exigido por el capítulo 25.
