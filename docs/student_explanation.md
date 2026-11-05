# Explicación conceptual para medicina, epidemiología e ingeniería estadística

## La idea en una frase

Antes de generar pacientes sintéticos, verificamos si disponemos de suficientes
estructuras independientes para representar las variantes clínicas de una GPC.

## Analogía con un protocolo epidemiológico

Imagina que planeas un estudio:

1. defines estados clínicos y criterios;
2. diseñas una ficha de recolección;
3. verificas que la ficha pueda representar cada estrato relevante;
4. recién después recolectas o simulas observaciones.

Generar datos antes del paso 3 sería como iniciar trabajo de campo y descubrir
al final que el instrumento no podía registrar una categoría importante.

En el proyecto:

| Epidemiología | Proyecto |
|---|---|
| protocolo clínico | GPC congelada |
| diagrama de estados | grafo dirigido \(D\) |
| estrato o trayectoria que se quiere representar | ClinicalRouteVariant |
| ficha parametrizable | estructura de caso clínico |
| verificación de elegibilidad | witness_assignment |
| plan de observaciones | assignment_manifest.json |
| base de datos | generación sintética futura |

La analogía ayuda, pero no es identidad: el matching no estima un efecto ni una
prevalencia.

## Tres niveles

### 1. Estructura de caso clínico

Es un esquema con variables y reglas:

- qué variables existen;
- qué valores pueden tomar;
- qué combinaciones son obligatorias o prohibidas;
- qué datos pueden faltar;
- qué estado inicial corresponde;
- de qué parte de la GPC proviene.

Todavía no hay una paciente concreta.

### 2. Instancia

Se asignan valores:

\[
c_1=1,\quad c_2=\cdots=c_7=0.
\]

La combinación determina una trayectoria sobre el grafo.

### 3. Registro sintético

Se realiza la instancia como texto, tabla o secuencia temporal. Este nivel no se
produce en el proyecto actual.

## La pregunta

> ¿Cómo asignar un catálogo finito de estructuras de caso clínico a variantes
> clínicas de ruta de una GPC, maximizando pares válidos uno-a-uno antes de
> generar datos sintéticos?

### “Catálogo finito”

No hablamos de una clase de software reutilizable infinitamente. Para el lote
piloto existen siete entradas disponibles y cada una tiene capacidad uno en el
manifiesto.

### “Variantes clínicas de ruta”

Una variante es una trayectoria completa y canónica:

    entrada → condición → decisión XOR → rama → terminal

Incluye predicados requeridos y prohibidos. Dos objetos con IDs distintos pero
la misma canonical_signature cuentan una sola vez.

### “Uno a uno”

Cada entrada del catálogo se reserva para una variante y cada variante recibe a
lo sumo una entrada:

\[
\sum_v x_{uv}\leq1,\qquad
\sum_u x_{uv}\leq1.
\]

Esta regla convierte el problema en matching bipartito.

## Dos grafos diferentes

### Grafo dirigido \(D\)

Responde:

> ¿Qué trayectoria sigue una combinación clínica?

Sus aristas significan transición o decisión.

### Grafo bipartito \(B\)

Responde:

> ¿Qué estructura puede representar qué variante?

Sus aristas significan compatibilidad demostrable.

Mezclar ambos grafos sería como mezclar el diagrama causal con la matriz que
asigna sujetos a estratos: cumplen funciones distintas.

## Cómo se acepta una arista

\[
(u,v)\in E
\iff
\exists x\in\operatorname{Inst}(u):
\operatorname{Exec}_D(x)=v.
\]

\(\operatorname{Exec}_D\) es parcial y determinista:

- si falta un dato necesario, rechaza;
- si hay contradicción, rechaza;
- si se habilitan dos ramas XOR, rechaza;
- si exactamente una rama puede seguirse hasta el terminal, devuelve la
  variante.

El \(x\) que demuestra la arista se guarda como witness_assignment. Decir que
dos textos “se parecen” no basta.

## Por qué las construcciones son independientes

Primero se enumeran variantes desde \(D\). En paralelo se construyen
estructuras desde el esquema de variables y restricciones. Después se prueban
todos los pares.

Si se construyera una estructura copiando cada variante, cada una tendría
garantizada su pareja y el grafo sería circular y trivial.

## La demo KISS

\[
U=\{S_1,\ldots,S_7\}
\]

\[
V=\{R_1,\ldots,R_7,R_0\}.
\]

- \(R_1,\ldots,R_7\): variantes con un criterio de severidad focal;
- \(R_0\): variante sin criterios de severidad.

Cada \(S_i\) puede producir:

- \(R_i\), con su criterio focal presente y los demás controlados;
- \(R_0\), con los siete ausentes.

Por tanto:

\[
E=\{(S_i,R_i),(S_i,R_0):1\leq i\leq7\}
\]

y:

\[
|U|=7,\quad|V|=8,\quad|E|=14.
\]

## Qué hace el matching

Un matching selecciona aristas sin repetir extremos. La cantidad de pares es la
cardinalidad \(|M|\).

Un matching maximal puede quedar bloqueado localmente sin ser el mayor posible.
Un matching máximo es el de mayor cardinalidad global.

## Camino aumentante

Supón:

    S1 — R1 seleccionada
    S2 libre
    R2 libre

Si existen las aristas \(S_2-R_1\) y \(S_1-R_2\), el camino:

\[
S_2-R_1-S_1-R_2
\]

permite reasignar y aumentar de uno a dos pares. CLRS expresa el cambio mediante
diferencia simétrica \(M\oplus P\).

El Corolario 25.4 dice que un matching es máximo si y solo si no existe camino
aumentante.

## Hopcroft-Karp

En lugar de aumentar un camino por vez:

1. BFS encuentra la longitud mínima;
2. DFS busca varios caminos mínimos disjuntos;
3. se aplican juntos;
4. se repite.

\[
T_{\mathrm{HK}}=O(m\sqrt n).
\]

Para siete por ocho, el beneficio práctico es irrelevante. Se usa porque
demuestra la teoría del curso y escala a catálogos mayores.

## Resultado

El algoritmo construye siete pares:

\[
|M^*|\geq7.
\]

Como solo hay siete estructuras:

\[
|M^*|\leq7.
\]

Entonces:

\[
|M^*|=7.
\]

## Hall explicado clínicamente

Las ocho variantes dependen de un catálogo con siete entradas:

\[
|S|=8>|N(S)|=7.
\]

No existe forma de entregar una estructura independiente a cada variante. Hall
formaliza esta insuficiencia.

No dice cuál variante debe excluirse. Sin pesos, cualquier óptimo puede dejar
una diferente.

## Qué contiene assignment_manifest.json

- versión y hash de la GPC;
- hash del grafo y reglas;
- estructura reservada;
- variante asignada;
- witness_assignment;
- restricciones invariantes;
- variante libre;
- déficit;
- estados de validación.

Es equivalente a un plan de muestreo estructural, no a la muestra obtenida.

## Dónde está la ingeniería estadística

- definición precisa de la unidad;
- control de linaje y versiones;
- prevención de leakage entre fuentes;
- separación entre estimando determinista e incertidumbre;
- validación de constructo;
- diseño prospectivo de métricas;
- análisis de sensibilidad a reglas;
- distinción entre fidelidad, utilidad y privacidad.

No se necesita forzar un valor p. Para un grafo fijo, \(|M^*|\) es exacto.

## Validez

### Algorítmica

¿El solver encuentra el óptimo?

### Estructural

¿Las variantes, estructuras, aristas y testigos son internamente consistentes?

### Clínica

¿Representan fielmente la GPC según especialistas independientes?

### Generativa

¿Los datos posteriores son coherentes, diversos, útiles y privados?

Una respuesta positiva no implica las demás.

## Cuándo cambiar de modelo

- una estructura cubre varias variantes: set cover;
- capacidades mayores que uno: \(b\)-matching;
- prioridades: matching ponderado;
- cuotas o prevalencias: programación entera;
- presupuesto fijo: maximum coverage.

## Respuesta oral

> Construimos las variantes desde el grafo de la GPC y, por separado, un
> catálogo de estructuras. Una arista existe solo si una asignación concreta
> ejecuta exactamente la variante. Hopcroft-Karp selecciona el mayor conjunto
> uno-a-uno. Con siete estructuras y ocho variantes, el óptimo es siete y Hall
> demuestra un déficit uno. El resultado es assignment_manifest.json, no un
> paciente sintético.
