# Informe KISS

## Una pregunta

> ¿Cuántas variantes clínicas de ruta de una GPC pueden recibir estructuras de
> caso distintas antes de generar datos sintéticos?

## Un grafo

\[
B=(U,V,E)
\]

- \(U\): siete entradas de un catálogo piloto de estructuras de caso sin texto,
  cada una con capacidad uno;
- \(V\): siete variantes severas focales y una variante sin severidad;
- \(E\): catorce posibilidades de instanciación demostradas.

Cada estructura \(S_i\) puede producir:

1. su ruta severa focal \(R_i\), activando el criterio correspondiente y
   controlando los demás;
2. la ruta común \(R_0\), fijando los siete criterios como ausentes.

Por eso:

\[
E=\{(S_i,R_i),(S_i,R_0):1\leq i\leq7\}.
\]

## Un algoritmo

Se calcula matching máximo de cardinalidad. El baseline encuentra caminos
aumentantes uno por uno. Hopcroft-Karp, siguiendo CLRS capítulo 25, usa BFS para
formar capas y DFS para encontrar varios caminos aumentantes mínimos por fase.

\[
T_{\mathrm{HK}}=O(|E|\sqrt{|U|+|V|}).
\]

## Un resultado

\[
|U|=7,\quad |V|=8,\quad |E|=14,\quad |M^*|=7.
\]

Existe un matching de siete pares y no puede existir uno mayor porque solo hay
siete estructuras. Para \(S=V\):

\[
|S|=8>|N(S)|=7.
\]

El déficit de Hall es uno.

## Una salida útil

El matching no genera un paciente. Produce **assignment_manifest.json**:

    estructura seleccionada
      + ruta reservada
      + valores testigo
      + restricciones invariantes
      + procedencia

Este objeto es la entrada controlada de una fase posterior de instanciación y
generación narrativa o tabular.

## Interpretación correcta

El resultado significa que siete rutas pueden recibir representantes
estructurales independientes. No significa:

- que una ruta sea más importante que otra;
- que la GPC esté clínicamente validada por el algoritmo;
- que los futuros pacientes sean realistas;
- que se haya medido una distribución poblacional.

## Hipótesis

Si todas las compatibilidades son correctas, el matching máximo crea el plan
uno-a-uno de mayor cardinalidad y Hall localiza la insuficiencia de capacidad.

## Aporte

Una capa combinatoria, trazable y previa a la generación que une:

    GPC computable
        → rutas clínicas
        → estructuras de caso
        → matching
        → assignment_manifest.json

La búsqueda dirigida encontró soporte para cada componente, pero no una
publicación que documente exactamente toda la integración. Se presenta como
prueba de concepto potencialmente novedosa y fundamentada, no como prioridad
mundial.

## Validación por capas

| Capa | Pregunta | Estado |
|---|---|---|
| algorítmica | ¿el solver encuentra el óptimo? | validada en la demo |
| estructural | ¿el grafo y Hall están bien construidos? | validada en la demo |
| clínica | ¿rutas, restricciones y aristas reflejan la GPC? | requiere panel |
| generativa | ¿las instancias son fieles, diversas, privadas y útiles? | futura |

## LOOP

    congelar → construir → ejecutar → emparejar
       ↑                              ↓
       └──── revisar ← validar ← manifestar

## Mensaje final

El bosque futuro son los datos sintéticos. Este proyecto describe bien un solo
árbol: comprobar, antes de generar, si cada ruta clínica dispone de una
estructura independiente y válida.
