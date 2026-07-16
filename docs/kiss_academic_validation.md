# Validación académica y científica — versión KISS

## Veredicto ejecutivo

El producto puede describirse hoy como:

> **prototipo educativo algorítmicamente validado, científicamente fundamentado
> y pendiente de validación experta y educativa.**

No puede describirse todavía como “clínicamente validado” ni como “efectivo para
mejorar aprendizaje”. Esas afirmaciones requieren datos que el proyecto aún no
ha recolectado.

## 1. Matriz afirmación-evidencia

| Afirmación | Evidencia actual | Estado |
|---|---|---|
| el grafo KISS tiene `7/8/14` | construcción declarativa + prueba directa | demostrada |
| el matching máximo vale 7 | DFS, Hopcroft-Karp, cota por `|U|` y Hall | demostrada |
| la brecha es estructural | `|S|=8>|N(S)|=7` | demostrada |
| el ejemplo procede del grafo completo | IDs, reglas y anexo técnico | demostrada |
| los casos son clínicamente coherentes | requiere panel experto | pendiente |
| los microobjetivos son pertinentes | requiere validez de contenido | pendiente |
| el método mejora un banco de casos | requiere comparación empírica | pendiente |
| el método mejora aprendizaje | requiere estudio con estudiantes | pendiente |
| generaliza a otras GPC | requiere replicación externa | pendiente |

## 2. Validez matemática

### Correctitud del objeto

Un matching es un conjunto de aristas sin endpoints repetidos. El objetivo es
maximizar su cardinalidad. Esta definición coincide con CLRS, capítulo 25, y con
la formulación clásica de matching máximo.

### Certificado de optimalidad

El subgrafo contiene siete casos. Por tanto, todo matching satisface `|M|≤7`.
Hopcroft-Karp y el baseline construyen siete pares, luego `|M|≥7`. Ambas cotas
coinciden.

El testigo de Hall agrega explicación: el conjunto de ocho objetivos tiene solo
siete vecinos. No existe un sistema de representantes distintos para todos los
objetivos.

### Complejidad

La implementación de Hopcroft-Karp sigue BFS por capas y DFS admisible. La cota
clásica es `O(E√V)` y el espacio es `O(V+E)`. Para este ejemplo pequeño, la
importancia es conceptual y no de velocidad.

## 3. Validez computacional

La versión KISS añade cuatro pruebas específicas:

1. conteos exactos `|U|=7`, `|V|=8`, `|E|=14` y `|M*|=7`;
2. dos aristas por caso: criterio propio y BPC común;
3. testigo único de Hall con déficit uno;
4. identidad entre el grafo construido por código y el JSON pequeño versionado.

Estas pruebas complementan la suite original, que compara dos solvers propios,
enumeración exhaustiva y NetworkX en 689 grafos pequeños. El oráculo externo se
usa para validación, no para producir el resultado presentado.

## 4. Validez de constructo

### Constructo medido

El indicador es **cobertura uno-a-uno de microobjetivos por representantes
compatibles y distintos**.

### Constructos que no mide

- calidad narrativa del caso;
- fidelidad clínica juzgada por expertos;
- aprendizaje o competencia;
- importancia relativa de objetivos;
- seguridad de decisiones clínicas;
- cobertura poblacional.

Llamar a `7/8=87,5 %` “cobertura educativa” es válido solo con esta definición
operacional. No debe abreviarse como “efectividad” o “validez clínica”.

## 5. Validez de contenido

La GPC sustenta los elementos fuente, pero no convierte automáticamente los
microobjetivos ni las viñetas en contenido educativo válido. La siguiente fase
usará un panel independiente para puntuar:

- fidelidad a la fuente;
- coherencia clínica;
- relevancia educativa;
- claridad;
- suficiencia de la arista caso-objetivo.

Se calcularán I-CVI y S-CVI/Ave con reglas preespecificadas. El protocolo está en
`docs/validation_protocol.md`; la plantilla de datos no contiene calificaciones
inventadas.

## 6. Validez educativa

El matching ayuda a construir el banco, pero su utilidad para docentes o
estudiantes es una hipótesis. Se propone una evaluación escalonada:

1. estudio de autoría con docentes: cobertura, redundancia y tiempo con y sin
   apoyo del grafo;
2. prueba de usabilidad;
3. piloto con estudiantes y desenlace alineado al objetivo;
4. replicación con otro cohorte antes de una afirmación fuerte.

Un aumento de cobertura estructural no implica por sí mismo un aumento de
aprendizaje.

## 7. Validez clínica

Este proyecto no toma decisiones sobre pacientes. Para un material educativo,
la pregunta clínica inmediata es **validez del contenido**, no beneficio sobre
resultados de pacientes. Un panel de obstetricia puede validar si cada escenario
es coherente y fiel a la versión de la guía.

Si en el futuro el sistema recomendara conductas o se usara en atención, el
nivel de evidencia requerido cambiaría por completo: validación externa,
evaluación prospectiva de seguridad, gobernanza y estudios de utilidad clínica.

## 8. Novedad calibrada

La revisión dirigida encontró antecedentes para cada bloque:

- grafos y modelos computables de GPC;
- simulaciones y viñetas clínicas asistidas por sistemas computacionales;
- matching máximo y certificados estructurales.

No se identificó, dentro de las fuentes y consultas registradas, una publicación
que combine exactamente los cinco pasos de este prototipo. La afirmación
permitida es:

> “La integración parece poco explorada y constituye una propuesta
> potencialmente novedosa dentro del alcance de nuestra revisión.”

La afirmación prohibida es:

> “Es el primer método del mundo” o “está científicamente validado”.

La prioridad universal solo podría sostenerse con una revisión sistemática más
amplia, búsquedas reproducibles en bases bibliográficas y cribado por pares.

## 9. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| confundir obligación estructural con objetivo curricular oficial | usar “microobjetivo diseñado a partir de la GPC” |
| regla uno-a-uno artificial | declarar el contexto: fichas, estaciones o representantes principales |
| priorización implícita por orden lexicográfico | no interpretar cuál objetivo queda fuera; ponderar en trabajo futuro |
| circularidad en la validación | revisores independientes y material cegado cuando sea viable |
| sobreafirmar novedad | publicar protocolo de búsqueda y lenguaje calibrado |
| confundir software correcto con contenido correcto | gates separados para algoritmo y panel clínico |

## 10. Conclusión

El núcleo matemático y computacional está validado en proporción al problema. La
base científica de los componentes está documentada. La validez clínica de
contenido y la utilidad educativa permanecen como hipótesis prospectivas con un
protocolo explícito, no como resultados simulados.
