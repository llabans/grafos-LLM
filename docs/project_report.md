# Informe del proyecto final

## Título

**Matching máximo entre estructuras de caso clínico y variantes de ruta de una guía como
paso previo a la generación de datos sintéticos**

## Resumen

Se diseñó una capa de asignación combinatoria entre una GPC estructurada y una
futura canalización de datos clínicos sintéticos. Las dos particiones del grafo
son entradas de un catálogo finito de estructuras de caso todavía no narradas y
variantes clínicas de ruta completas,
canónicas y trazables. Una arista existe solo si se demuestra una instancia de
la estructura cuya ejecución recorre exactamente la ruta. El matching máximo
reserva pares uno-a-uno y produce **assignment_manifest.json**.

La instancia KISS utiliza siete estructuras, ocho rutas y catorce aristas. Las
rutas comprenden siete trayectorias con un criterio de severidad focal y una
trayectoria sin severidad. Cada estructura puede instanciar su ruta focal o la
ruta común sin severidad. El baseline por caminos aumentantes y Hopcroft-Karp
obtienen cardinalidad siete. La cota por \(|U|\) y el testigo de Hall
\(8>7\) certifican que no pueden asignarse las ocho rutas sin reutilización.

## Problema

Una GPC computable puede enumerar rutas, pero eso no implica que exista una
estructura independiente capaz de generar cada una. Generar narrativas primero
y revisar después desplaza errores lógicos hacia una etapa costosa. El proyecto
interpone una auditoría previa:

1. formalizar rutas;
2. definir estructuras permitidas;
3. demostrar compatibilidades;
4. optimizar la asignación;
5. registrar la brecha antes de generar.

## Pregunta y objetivo

> ¿Cómo asignar un catálogo finito de estructuras de caso clínico a variantes
> clínicas de ruta de una GPC para maximizar el número de asignaciones válidas
> uno-a-uno antes de generar casos sintéticos?

El objetivo es construir \(B=(U,V,E)\), calcular un matching máximo y producir
un manifiesto trazable con pares, testigos y rutas no asignadas.

## Hipótesis

Si las estructuras y rutas son válidas y cada arista se prueba por ejecución,
Hopcroft-Karp devolverá el máximo número de pares independientes y los déficits
de Hall identificarán falta de capacidad estructural.

## Material

Se trabaja con una sola GPC de hipertensión en el embarazo, congelada en el
pipeline privado. La demostración pública reemplaza textos e identificadores
clínicos por IDs simbólicos, pero conserva la topología \(7-8-14\).

No se mezclan otras guías ni conocimiento médico externo.

## Formulación

\[
\max |M|,\qquad M\subseteq E,
\]

con grados en \(M\) no mayores que uno para todo vértice de \(U\cup V\).
La compatibilidad se define por:

\[
(u,v)\in E
\iff
\exists x\in\operatorname{Inst}(u):
\operatorname{Exec}_D(x)=v.
\]

## Fundamento algorítmico

La fuente principal es CLRS, cuarta edición, capítulo 25. Un camino aumentante
permite sustituir \(M\) por \(M\oplus P\) y aumentar su tamaño en uno. La
ausencia de caminos aumentantes caracteriza un matching máximo. Hopcroft-Karp
procesa por fase un conjunto maximal de caminos aumentantes mínimos disjuntos y
alcanza \(O(|E|\sqrt{|V_B|})\).

El proyecto no usa matrimonio estable: no existen rankings bilaterales. Tampoco
usa matching ponderado: la versión KISS optimiza cardinalidad.

## Resultado

| Métrica | Valor |
|---|---:|
| \(|U|\) | 7 |
| \(|V|\) | 8 |
| \(|E|\) | 14 |
| \(|M^*|\) | 7 |
| déficit de Hall | 1 |

La optimalidad se demuestra por una solución factible de siete y una cota
superior de siete. Para todas las rutas \(S=V\), \(N(S)=U\), por lo que
\(|S|>|N(S)|\).

## Producto operativo

El matching se transforma en **assignment_manifest.json**, que especifica:

- qué estructura queda reservada para qué ruta;
- qué valores testigo producen la ruta;
- qué restricciones no pueden alterarse;
- qué fuente y versión sustentan la asignación;
- qué ruta queda libre;
- qué validaciones se han completado.

La selección concreta no es única. Cualquier matching de cardinalidad siete es
óptimo, pero un solver no ponderado no expresa prioridad clínica.

## Aporte

El aporte no es un nuevo algoritmo. Es una aplicación trazable de teoría
clásica a una interfaz poco documentada: entre la formalización de una GPC y la
generación sintética. El grafo permite detectar antes de generar:

- rutas sin estructura compatible;
- competencia colectiva por estructuras;
- capacidad insuficiente;
- necesidad de ampliar estructuras o cambiar de modelo.

## Validez

### Demostrado

- correctitud algorítmica de la asignación para el grafo fijado;
- cardinalidad óptima y déficit;
- reproducibilidad de la demo pública;
- separación entre fuente, compatibilidad y solver.

### Pendiente

- revisión clínica independiente de rutas, estructuras y testigos;
- validación de la reconstrucción completa contra la fuente privada;
- generación y evaluación de instancias;
- fidelidad distribucional, diversidad, privacidad y utilidad analítica;
- transportabilidad a otra GPC.

## Relación con la literatura

Peleg et al. y GLIF3 sustentan las representaciones computables de guías.
Synthea muestra que GPC y máquinas de estados pueden alimentar generación de
pacientes sintéticos, pero también que procedencia no garantiza realismo.
CPGPrompt aporta un antecedente reciente para traducir guías a árboles
ejecutables. CLRS y Hopcroft-Karp proporcionan la teoría de asignación.

La búsqueda dirigida no identificó la cadena exacta GPC → rutas → estructuras
de caso → compatibilidad demostrable → matching → manifiesto. Esta ausencia es
una observación del alcance revisado, no una afirmación de prioridad mundial.

## Limitaciones

- una sola GPC;
- topología KISS pequeña y preespecificada;
- estructuras y variantes públicas simbólicas;
- capacidades unitarias deliberadas;
- ausencia de pesos clínicos;
- datos sintéticos todavía no generados;
- validez condicionada a la exactitud de las aristas.

## Conclusión

Siete estructuras independientes pueden reservarse para siete de ocho rutas. El
déficit se conoce antes de generar un solo paciente sintético. Esta es la
utilidad del proyecto: convertir una brecha potencialmente oculta en una
propiedad combinatoria reproducible, explicable y accionable.
