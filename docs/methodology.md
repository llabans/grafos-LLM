# Metodología

## Diseño

Prueba de concepto algorítmico-estructural, reproducible y de una sola GPC. La
unidad de análisis es una compatibilidad entre una entrada del catálogo de
estructuras y una variante clínica de ruta. El estimando computacional es la cardinalidad del matching
máximo del grafo fijado; no es un parámetro poblacional.

## GOAL

Construir el mayor **assignment_manifest.json** uno-a-uno de pares
estructura-variante que puedan instanciarse de forma lógica y trazable antes de
generar datos clínicos sintéticos.

## LOOP

    CONGELAR FUENTE
        ↓
    EXTRAER Y RECONCILIAR
        ↓
    CONSTRUIR VARIANTES DE RUTA
        ↓
    DEFINIR ESTRUCTURAS
        ↓
    DEMOSTRAR COMPATIBILIDADES
        ↓
    RESOLVER MATCHING
        ↓
    VERIFICAR Y VALIDAR
        ↺

Cada vuelta conserva versiones y no sobrescribe silenciosamente evidencia
previa.

## 1. Congelamiento de la fuente

Se fija una sola GPC mediante:

- identificador estable;
- versión y fecha;
- inventario de archivos;
- hashes SHA-256;
- secciones, páginas y unidades de conocimiento;
- reglas de normalización.

La demo pública emplea IDs simbólicos. La reconstrucción clínica exacta requiere
el snapshot privado y superar sus verificaciones de hash.

## 2. Reconciliación de representaciones

La GPC estructurada incluye flujogramas primarios, grafos derivados, unidades
clínicas y recomendaciones. Los flujogramas se tratan como autoridad para
transiciones; las representaciones derivadas sirven para reconciliar IDs,
inicios, terminales y procedencia. Una discrepancia activa un error de fuente,
no una imputación.

## 3. Grafo dirigido de decisión

Se construye \(D=(N,A)\), donde los nodos representan estados, condiciones,
decisiones o acciones y las aristas representan transiciones autorizadas. Se
verifica:

- entrada y terminales definidos;
- alcanzabilidad desde la entrada;
- etiquetas de rama no ambiguas;
- ausencia de referencias colgantes;
- consistencia de predicados;
- trazabilidad de cada nodo y transición.

Este grafo dirigido modela la lógica clínica. No debe confundirse con el grafo
bipartito de asignación.

## 4. Variantes clínicas de ruta por representar

De \(D\) se enumeran variantes completas, canónicas, alcanzables y no
redundantes:

    estado inicial
        → condición
        → decisión
        → rama
        → acción o terminal

Cada **ClinicalRouteVariant** registra:

- identificador;
- estado de entrada;
- predicados requeridos y prohibidos;
- nodo de decisión y rama;
- acción terminal;
- unidades fuente y páginas;
- estado de validación.

La deduplicación se realiza mediante **canonical_signature**, que ignora el ID y
usa la secuencia canónica de estados, predicados, ramas y terminal. No se usa
parecido textual.

## 5. Estructuras de caso clínico

Se construye un catálogo finito para el lote piloto. Cada entrada tiene
capacidad uno en este matching y contiene:

- variables clínicas autorizadas por la GPC;
- tipos y dominios posibles;
- restricciones obligatorias;
- combinaciones prohibidas;
- missingness permitido;
- estado inicial;
- procedencia;
- estado de validación.

Las estructuras se derivan del esquema de variables, dominios y restricciones,
no de las variantes ya enumeradas. Así se evita fabricar una estructura a la
medida de cada ruta y volver trivial el grafo.

En esta fase no se agregan nombres, edades de relleno, prosa, eventos no
sustentados ni conocimiento clínico externo.

## 6. Oráculo de compatibilidad

Para cada par \((u,v)\), el oráculo busca un \(x\in\operatorname{Inst}(u)\) tal
que \(\operatorname{Exec}_D(x)=v\). \(\operatorname{Exec}_D\) es parcial,
determinista y recorre decisiones XOR: una asignación válida habilita exactamente
una rama; missingness insuficiente o contradicción produce rechazo. La decisión
debe ser:

- determinista;
- reproducible;
- explicable;
- acompañada por **witness_assignment** positivo y persistido;
- acompañada por código de rechazo cuando no existe testigo.

Los códigos de rechazo distinguen variable ausente, dominio insuficiente,
predicado contradictorio, terminal inaccesible y procedencia incompleta.

## 7. Construcción de \(B=(U,V,E)\)

Se valida que:

- \(U\cap V=\varnothing\);
- cada arista tenga un extremo en cada partición;
- no existan duplicados;
- todos los IDs referidos existan;
- cada arista tenga testigo y versión de regla;
- los aislados se conserven, porque son resultados informativos.

## 8. Algoritmos de matching

### Baseline por caminos aumentantes

Se inicia con \(M=\varnothing\). Mientras exista un camino
\(M\)-aumentante \(P\), se reemplaza \(M\) por \(M\oplus P\). El Lema 25.1 de
CLRS muestra que cada aumento incrementa la cardinalidad en uno, y el Corolario
25.4 certifica que la ausencia de caminos aumentantes equivale a optimalidad.

Con búsqueda lineal por aumento, el costo usado como referencia es
\(O(|U||E|)\), incluido en \(O(|V_B||E|)\).

### Hopcroft-Karp

El algoritmo agrupa caminos aumentantes mínimos y disjuntos por vértices:

1. BFS construye capas de distancias alternantes;
2. DFS recorre solo aristas admisibles en esas capas;
3. la diferencia simétrica aumenta \(M\) por todos los caminos hallados;
4. se repite hasta que no exista camino aumentante.

CLRS, capítulo 25, demuestra la cota:

\[
O(|E|\sqrt{|V_B|}).
\]

En la instancia KISS la ventaja temporal no es necesaria por tamaño, pero su
implementación evidencia comprensión del algoritmo solicitado.

## 9. Certificados

Se reportan:

- matching completo;
- cardinalidad;
- verificación de unicidad;
- ausencia de caminos aumentantes;
- acuerdo entre baseline, Hopcroft-Karp y un oráculo independiente;
- conjunto de Hall cuando existe déficit.

Para la demo, \(S=V\) tiene ocho rutas y siete estructuras vecinas. El déficit
es uno.

## 10. assignment_manifest.json

Cada par seleccionado se serializa en **assignment_manifest.json** con:

- estructura reservada;
- ruta asignada;
- witness_assignment persistido;
- restricciones que deben permanecer invariantes;
- fuente y hashes;
- semilla de generación futura;
- estado de revisión.

Una ruta libre también se registra. No se inventa una estructura para completar
el conteo.

## 11. Estrategia de verificación

1. pruebas unitarias de estructuras de datos;
2. grafos límite: vacío, aislado, perfecto, múltiple y deficitario;
3. enumeración exhaustiva de grafos pequeños;
4. concordancia con un solver externo;
5. prueba de permutación de IDs;
6. repetibilidad del JSON;
7. ejecución de cada testigo sobre \(D\);
8. reconstrucción desde la fuente congelada cuando esté disponible.

## 12. Complejidad del pipeline

Sea \(n=|U|+|V|\), \(m=|E|\) y \(C_{\mathrm{compat}}\) el costo máximo de
evaluar un par. La cota de ingeniería es:

\[
T_{\mathrm{total}}=
T_{\mathrm{routes}}+
T_{\mathrm{structures}}+
O(|U||V|C_{\mathrm{compat}})+
O(n+m\sqrt n).
\]

El último sumando incluye inicialización y Hopcroft-Karp; la parte dominante del
solver es \(O(m\sqrt n)\). La construcción exhaustiva de compatibilidades puede
dominar el tiempo total.

## 13. Análisis estadístico proporcionado

La cardinalidad del matching es exacta y determinista para un grafo fijado; no
corresponde calcular un intervalo de confianza. La incertidumbre aparece en las
aristas clínicas y en los datos sintéticos posteriores.

Para la validación experta se reportarán acuerdo, I-CVI, S-CVI/Ave, kappa
modificado cuando corresponda y todas las discordancias. Para la fase generativa
se preespecificarán métricas de fidelidad lógica, distribución, diversidad y
privacidad. No se realizarán pruebas de hipótesis sobre tiempos de ejecución con
repeticiones no independientes.

## 14. Reproducibilidad

El repositorio conserva código, pruebas, documentación, notebook, manifiestos y
artefactos de exposición. Los resultados clínicamente identificables no se
publican; se publica una demo simbólica con la misma topología.

## 15. Criterio de finalización

El proyecto se considera completo para el curso cuando:

- la pregunta y las particiones son inequívocas;
- las catorce aristas de la demo tienen testigos;
- ambos algoritmos devuelven siete;
- el déficit de Hall es reproducible;
- el manifiesto no repite estructuras ni rutas;
- los límites de validez se declaran;
- teoría, análisis, aplicación, código, Colab, material y exposición cubren la
  rúbrica.
