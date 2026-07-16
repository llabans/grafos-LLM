# Iteración 0: inspección y congelamiento

## Objetivo

Fijar fuente, teoría, rúbrica, semántica y límites antes de modificar el
software.

## Material inspeccionado

- snapshot estructurado de una GPC;
- flujogramas, recomendaciones, tablas y estructura;
- archivos Phase 4 filtrados por source_id;
- CLRS, cuarta edición, capítulo 25;
- indicaciones del proyecto final;
- repositorio y artefactos existentes.

## Rúbrica fijada

La entrega requiere:

- teoría;
- análisis;
- aplicación;
- código;
- notebook Colab;
- material adicional;
- exposición de 15 minutos.

Estos requisitos se traducen en gates verificables, no solo en secciones de una
presentación.

## Decisiones semánticas

1. Usar una sola GPC.
2. Modelar la lógica con un grafo dirigido \(D\).
3. Limitar KISS al subgrafo XOR de flow_2.
4. Definir \(V\) como variantes clínicas de ruta por representar.
5. Definir \(U\) como catálogo finito de estructuras para un lote piloto.
6. Construir rutas y estructuras por vías independientes.
7. Aceptar una arista solo con witness_assignment reproducible.
8. Finalizar el proyecto en assignment_manifest.json.

## Tres niveles

| Nivel | Existe en esta entrega |
|---|---|
| estructura de caso | sí |
| instancia con valores | solo testigo mínimo de compatibilidad |
| caso o registro sintético completo | no |

## Instancia acordada

\[
|U|=7,\quad |V|=8,\quad |E|=14,\quad |M^*|=7.
\]

Las variantes son siete rutas severas focales y una sin severidad. Cada entrada
del catálogo admite su ruta focal y la ruta común sin severidad.

## Construcción no circular

- \(V\) se enumera desde \(D\) y se deduplica por canonical_signature.
- \(U\) se construye desde variables, dominios y restricciones permitidas.
- \(E\) se construye después, evaluando todos los pares.

Construir una estructura directamente desde cada variante haría trivial la
compatibilidad y debilitaría el aporte.

## Complejidad prevista

\[
T_{\mathrm{total}}=
T_{\mathrm{routes}}+
T_{\mathrm{structures}}+
O(|U||V|C_{\mathrm{compat}})+
O(n+m\sqrt n).
\]

## Riesgos identificados

- confundir estructura con paciente;
- llamar objetivo a una variante;
- considerar una estructura como tipo reutilizable sin declarar capacidad;
- aceptar similitud semántica como arista;
- confundir Hall con validación clínica;
- circularidad en la construcción;
- exponer contenido privado;
- afirmar utilidad sintética antes de generar datos.

## Gates

- [x] capítulo 25 localizado;
- [x] rúbrica registrada;
- [x] una GPC y subgrafo definidos;
- [x] particiones reformuladas;
- [x] topología KISS acordada;
- [x] implementación alineada con ClinicalRouteVariant;
- [x] witness_assignment persistido;
- [x] assignment_manifest.json reproducible;
- [x] documentación y presentación sincronizadas.

Estos gates se cerraron en las iteraciones posteriores y se reejecutaron sobre
los artefactos finales; los pendientes clínicos y generativos se mantienen
explícitos.
