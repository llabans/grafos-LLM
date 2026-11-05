# Validación académica y científica

## Estado de la afirmación

El producto puede describirse como:

> **prueba de concepto pre-generativa, algorítmicamente validada,
> estructuralmente verificable y pendiente de validación clínica y generativa.**

No debe describirse como generador de pacientes clínicamente válidos porque el
alcance termina antes de la instanciación masiva.

## Matriz afirmación-evidencia

| Afirmación | Evidencia requerida | Estado |
|---|---|---|
| el algoritmo encuentra matching máximo | pruebas, oráculo y certificado | demostrado en la demo |
| la cardinalidad es siete | solución factible y cota superior | demostrado |
| no existe matching perfecto | testigo de Hall \(8>7\) | demostrado |
| cada arista posee testigo ejecutable | ejecución contra \(D\) | verificable; depende de fuente local para reconstrucción clínica |
| variantes y restricciones reflejan la GPC | revisión de fuente y panel clínico | pendiente de panel independiente |
| assignment_manifest.json mejora la generación | comparación prospectiva | pendiente |
| los datos futuros serán fieles y privados | evaluación generativa multidimensional | fuera del alcance actual |

## Validez algorítmica

Un matching es un conjunto de aristas sin extremos repetidos. Según CLRS,
capítulo 25, la diferencia simétrica con un camino aumentante incrementa la
cardinalidad en uno. Cuando no existe camino aumentante, el matching es máximo.

La validación exige:

- baseline por caminos aumentantes;
- Hopcroft-Karp;
- comparación con solver independiente;
- enumeración exhaustiva de grafos pequeños;
- invariancia ante renombramiento de vértices;
- ausencia de duplicados en la salida.

La concordancia de software no valida las aristas clínicas.

## Validez estructural

Se inspeccionan:

- disjunción de \(U\) y \(V\);
- aristas únicamente entre particiones;
- rutas alcanzables y completas;
- testigo positivo por arista;
- aislados conservados;
- conteos \(7-8-14\);
- matching de siete;
- déficit de Hall uno.

El constructo es **capacidad uno-a-uno pre-generativa**. La razón \(7/8\) no es
sensibilidad, exactitud, cobertura poblacional ni prevalencia.

## Validez clínica

Un panel independiente debe evaluar:

1. fidelidad de cada ruta a la GPC;
2. suficiencia y permisibilidad de variables;
3. coherencia de restricciones;
4. corrección del witness_assignment persistido;
5. exclusión de combinaciones contraindicadas;
6. trazabilidad de nodos, páginas y unidades fuente.

Los índices I-CVI y S-CVI/Ave pueden resumir acuerdo, pero deben acompañarse de
distribuciones, comentarios, adjudicación y versión posterior. El juicio del
equipo desarrollador o de un LLM no reemplaza revisión clínica independiente.

## Validez generativa

Solo cuando existan instancias sintéticas se evaluarán:

- ejecución exacta de la variante asignada;
- violaciones de restricciones;
- consistencia clínica y temporal;
- fidelidad marginal, conjunta y longitudinal;
- diversidad y duplicación;
- utilidad downstream;
- privacidad y riesgo de divulgación.

Synthea, Zhang et al. y Zhou et al. muestran por vías diferentes que procedencia,
fidelidad estadística y consistencia clínica no son equivalentes.

## Correctitud de la instancia KISS

Cada estructura \(S_i\) tiene dos testigos:

- severo: criterio \(i=1\) y demás criterios controlados, que ejecuta \(R_i\);
- no severo: los siete criterios \(=0\), que ejecuta \(R_0\).

Esto produce catorce aristas. El solver construye siete pares. Como ningún
matching puede superar \(|U|=7\), el resultado es óptimo. Para \(S=V\),
\(|S|=8>|N(S)|=7\), luego no existe matching que sature las ocho variantes.

## Hipótesis científicas proporcionadas

### H1 algorítmica

La implementación devuelve el óptimo para grafos bipartitos válidos.

### H2 estructural

Toda arista aceptada corresponde a una instanciación que ejecuta exactamente la
ruta declarada.

### H3 clínica

Los especialistas aceptan rutas, restricciones y testigos como fieles a la GPC.

### H4 generativa futura

Usar **assignment_manifest.json** reduce omisiones de variantes y violaciones
lógicas frente a una generación directa sin capa de asignación.

H4 requiere comparación prospectiva y no se infiere de H1-H3.

## Novedad calibrada

La literatura apoya los bloques de la propuesta. La ausencia de un trabajo que
integre exactamente todos los pasos es una inferencia de búsqueda dirigida. El
lenguaje admisible es “integración potencialmente novedosa” y no “primer método
mundial”.

## Adecuación al nivel de maestría

El trabajo:

- formula un problema de optimización con supuestos explícitos;
- implementa y contrasta algoritmos;
- separa estimando determinista e incertidumbre clínica;
- usa certificados, no solo salidas;
- propone un protocolo prospectivo;
- discute validez interna, externa y de constructo;
- limita inferencias y evita confundir verificación con validación.

## Conclusión

La evidencia es suficiente para defender el matching y el déficit en la demo.
La afirmación clínica queda condicionada al panel; la afirmación sobre calidad
de datos queda diferida hasta que exista una generación evaluable.
