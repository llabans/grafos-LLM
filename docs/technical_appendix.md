# Apéndice técnico de la instancia KISS

## Topología

\[
U=\{S_1,\ldots,S_7\},
\qquad
V=\{R_1,\ldots,R_7,R_0\}.
\]

\[
E=\{(S_i,R_i),(S_i,R_0):1\leq i\leq7\}.
\]

Así, \(|U|=7\), \(|V|=8\) y \(|E|=14\).

## Semántica de una estructura

Cada \(S_i\) declara siete variables binarias de severidad:

\[
\mathbf{c}=(c_1,\ldots,c_7).
\]

Su testigo severo focal es:

\[
x_i^{+}: c_i=1,\quad c_j=0\ \text{para}\ j\neq i.
\]

Su testigo para ausencia de severidad es:

\[
x_i^{0}: c_1=\cdots=c_7=0.
\]

La semántica clínica completa incluye estado de entrada, otros predicados y
acción terminal; se omite de la demo pública por desidentificación y KISS.

## Regla de arista

\[
\operatorname{Exec}_D(x_i^{+})=R_i,
\qquad
\operatorname{Exec}_D(x_i^{0})=R_0.
\]

No se incluyen aristas \((S_i,R_j)\) con \(i\neq j\) porque \(S_i\) no declara
como parametrizable el criterio focal \(j\) bajo la versión preespecificada.

## Matching de ejemplo

Un matching máximo posible es:

\[
M=\{(S_1,R_0),(S_2,R_2),\ldots,(S_7,R_7)\}.
\]

Otra solución puede dejar libre cualquiera de las rutas, porque el problema no
tiene pesos. El valor óptimo sí es único:

\[
|M^*|=7.
\]

## Certificado de Hall

Sea \(S=V\). Todas las rutas tienen como vecinos las siete estructuras:

\[
N(S)=U.
\]

Entonces:

\[
\delta(S)=|S|-|N(S)|=8-7=1.
\]

No existe matching que sature \(V\).

## Relación con CLRS

- Definición de matching: cada vértice tiene a lo sumo una arista incidente en
  \(M\).
- Lema 25.1: \(M\oplus P\) aumenta la cardinalidad en uno.
- Corolario 25.4: ausencia de camino aumentante equivale a máximo.
- Hopcroft-Karp: conjunto maximal de caminos aumentantes mínimos disjuntos por
  vértices en cada fase.
- Teorema 25.8: \(O(|E|\sqrt{|V_B|})\).
- Ejercicio 25.1-5: condición de Hall.

## assignment_manifest.json mínimo propuesto

    {
      "source_id": "...",
      "source_hash": "...",
      "graph_hash": "...",
      "algorithm": "hopcroft_karp",
      "matching_size": 7,
      "assignments": [
        {
          "case_structure_id": "S1",
          "clinical_route_id": "R0",
          "witness": {"c1": 0, "...": 0}
        }
      ],
      "unassigned_routes": ["..."],
      "hall_deficiency": 1,
      "validation": {
        "algorithmic": "passed",
        "structural": "passed",
        "clinical": "pending",
        "generative": "not_started"
      }
    }

## Extensiones

- pesos: matching de peso máximo;
- varias instancias por estructura: \(b\)-matching;
- reutilización para cubrir rutas: set cover;
- prevalencias y cuotas: programación entera;
- probabilidad de ejecución: aristas ponderadas por robustez;
- múltiples GPC: grafos separados con análisis de transportabilidad.
