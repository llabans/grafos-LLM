# Guion de presentación KISS: 15 minutos

## Resultado que debe comprender la audiencia

Un grafo bipartito puede auditar la capacidad de un catálogo de estructuras de
caso clínico antes de generar datos sintéticos. El algoritmo produce un
manifiesto óptimo y explica la brecha, pero no valida pacientes.

## Distribución temporal

| # | Tiempo | Título del PPT | Propósito |
|---:|---:|---|---|
| 1 | 0:50 | Siete estructuras. Ocho variantes. | tensión, pregunta y GOAL |
| 2 | 1:35 | El grafo trabaja antes de crear pacientes sintéticos | distinguir el grafo clínico dirigido del bipartito |
| 3 | 1:35 | Cada estructura se reserva para una sola variante | formalizar (U,V,E), capacidad y objetivo |
| 4 | 1:40 | Reasignar una estructura puede abrir otra variante | explicar camino aumentante y optimalidad |
| 5 | 1:40 | Hopcroft-Karp agrupa aumentos mínimos por fase | algoritmo y complejidad CLRS |
| 6 | 2:15 | Siete estructuras no asignan ocho variantes uno a uno | mostrar resultado, cotas y Hall |
| 7 | 1:55 | El Colab reproduce el óptimo y sus testigos | código, pruebas y manifiesto |
| 8 | 1:55 | El matching es una compuerta, no un generador | ubicar la contribución y sus límites |
| 9 | 1:05 | Siete estructuras asignan como máximo siete variantes | responder, cerrar y señalar la siguiente fase |
|  | **14:30** |  | **0:30 de contingencia hasta 15:00** |

## Diapositiva 1. Siete estructuras. Ocho variantes.

Pregunta oral:

> Antes de generar datos sintéticos, ¿cuántas variantes clínicas pueden recibir
> una estructura compatible y exclusiva?

GOAL:

> Maximizar variantes representadas con estructuras distintas y emitir
> assignment_manifest.json.

Aclaración inmediata: todavía no hay pacientes, narrativas ni registros
sintéticos completos.

## Diapositiva 2. El grafo trabaja antes de crear pacientes

- (D), grafo dirigido: decide qué trayectoria ejecuta una asignación de
  valores.
- (B), grafo bipartito: decide qué estructura puede reservarse para qué
  variante.
- (U): variables, dominios, restricciones, missingness y procedencia.
- (V): variante identificada por ruta y firma de predicados.
- (E): compatibilidad con witness_assignment reejecutable.

Mensaje: una transición clínica y una arista de compatibilidad responden
preguntas distintas.

## Diapositiva 3. Reserva uno-a-uno

Presentar:

\[
\max \sum_{(u,v)\in E}x_{uv}
\]

sujeto a:

\[
\sum_v x_{uv}\leq1\quad\forall u,
\qquad
\sum_u x_{uv}\leq1\quad\forall v.
\]

La capacidad uno pertenece al lote piloto. La firma canónica bloquea clones
obtenidos cambiando solo un ID. Matching máximo no significa matching maximal.

## Diapositiva 4. Camino aumentante

Recorrer el ejemplo:

\[
E_2-V_1-E_1-V_2.
\]

- alterna aristas que no están y que sí están en (M);
- comienza y termina en vértices libres;
- (M'=M\oplus P) aumenta la cardinalidad en uno.

Base CLRS:

- Lema 25.1: la diferencia simétrica conserva matching y suma uno;
- Corolario 25.4: (M) es máximo si y solo si no existe camino aumentante.

## Diapositiva 5. Hopcroft-Karp

1. BFS construye capas de distancia mínima.
2. DFS busca caminos aumentantes admisibles y disjuntos.
3. La fase aumenta todos los encontrados.
4. Se repite hasta no encontrar otro camino aumentante.

\[
T_{\mathrm{HK}}=O(m\sqrt n),
\qquad
T_{\mathrm{implementación}}=O(n+m\sqrt n).
\]

El costo completo del pipeline también incluye derivación de variantes,
construcción de estructuras y materialización de (E).

## Diapositiva 6. Resultado y prueba

\[
|U|=7,\quad|V|=8,\quad|E|=14,\quad|M^*|=7.
\]

- cota inferior: se exhiben siete pares factibles;
- cota superior: solo existen siete estructuras-cupo;
- Hall: para (S=V), (|S|=8>|N(S)|=7), déficit uno.

Hall explica por qué una variante queda libre, pero no cuál es menos importante
clínicamente.

## Diapositiva 7. Código y Colab

La demo muestra únicamente:

1. construcción determinista de (B);
2. catorce aristas con testigo;
3. DFS aumentante (=7);
4. Hopcroft-Karp (=7);
5. NetworkX (=7) como oráculo independiente;
6. testigo de Hall y assignment_manifest.json.

La fuente clínica privada no se expone.

## Diapositiva 8. Compuerta previa a síntesis

Cadena fundamentada:

- Peleg y GLIF3: GPC computables;
- Synthea: mapas clínicos y máquinas de estados;
- CPGPrompt: guía a árbol ejecutable y dificultad en rutas finas;
- CLRS: asignación bipartita óptima.

Contribución calibrada:

> El proyecto inserta una compuerta combinatoria auditable antes de instanciar
> o narrar. La búsqueda dirigida no identificó la integración exacta completa;
> esto no demuestra prioridad mundial.

Separar validez algorítmica, estructural, clínica y generativa.

## Diapositiva 9. Respuesta y cierre

> Con siete estructuras-cupo pueden asignarse como máximo siete de ocho
> variantes. La salida es un manifiesto pre-generativo con pares, testigos,
> procedencia y la variante no asignada.

Estado:

- demostrado: matching, cardinalidad y Hall;
- fundamentado: GPC computables y simulación por estados;
- pendiente: revisión clínica experta y validez generativa, temporal y
  estadística.

Siguiente paso: revisar contenido con panel clínico, instanciar un lote piloto y
validarlo antes de narrar.

## Preguntas probables

### ¿Por qué no generar directamente?

Porque una narración fluida puede incumplir la lógica de la ruta. La compuerta
previa detecta falta de capacidad o contradicción de forma más barata y
auditable.

### ¿Por qué matching?

Porque el lote exige una estructura independiente por variante y capacidad
uno. Si se permite reutilización, cambia el modelo: por ejemplo, (b)-matching
o cobertura de conjuntos según la pregunta.

### ¿Por qué siete es máximo?

Existe un matching de siete y (|U|=7) es una cota superior. El Corolario 25.4
certifica el solver; Hall explica la imposibilidad de saturar las ocho
variantes.

### ¿Cuál variante queda fuera?

El modelo no ponderado no expresa prioridad clínica; distintas soluciones
óptimas pueden dejar libre una variante diferente.

### ¿La estructura es reutilizable?

El tipo de software podría reutilizarse. En este modelo, cada (u\in U)
representa un cupo concreto del catálogo piloto y declara capacidad uno.

### ¿Está clínicamente validado?

No completamente. Solver, topología y testigos se verificaron; rutas,
restricciones y contenido de los testigos requieren revisión experta
independiente.

### ¿Es pionero?

Es una integración potencialmente novedosa según una búsqueda dirigida, no una
afirmación de prioridad mundial.

## Corte si falta tiempo

- reducir el ejemplo del camino aumentante a una sola reasignación;
- mencionar, sin derivar, la cota de Hopcroft-Karp;
- conservar completas las diapositivas 2, 6, 7 y 9.
