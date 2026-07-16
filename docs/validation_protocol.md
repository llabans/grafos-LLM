# Protocolo prospectivo de validación

## Objetivo

Validar por separado:

1. correctitud algorítmica;
2. consistencia estructural del grafo;
3. fidelidad clínica a la GPC;
4. desempeño generativo futuro.

El protocolo no valida un sistema de soporte a decisiones ni autoriza uso con
pacientes reales.

## Fase 0. Registro y congelamiento

Antes de revisar resultados:

- congelar GPC, archivos y hashes;
- versionar \(D\), \(U\), \(V\), reglas y testigos;
- registrar hipótesis y umbrales;
- definir el uso previsto de los futuros datos;
- separar desarrolladores, revisores clínicos y analistas cuando sea posible;
- conservar todas las discordancias.

## Fase 1. Verificación algorítmica

### Unidades

- grafos de prueba;
- demo \(7-8-14\);
- salida de baseline;
- salida de Hopcroft-Karp;
- oráculo independiente.

### Gates

- cardinalidades idénticas;
- matching válido;
- ausencia de camino aumentante al terminar;
- serialización determinista;
- concordancia exhaustiva en grafos pequeños;
- invariancia ante permutación de IDs.

Un fallo bloquea las fases posteriores.

## Fase 2. Validación estructural

### Unidades

- ocho variantes clínicas de ruta;
- siete estructuras;
- catorce aristas;
- catorce testigos positivos;
- muestra preespecificada de pares rechazados.

### Pruebas

- cada ruta inicia y termina correctamente;
- cada predicado es satisfacible;
- cada testigo cumple dominios y restricciones;
- \(\operatorname{Exec}_D(x)=v\), con ejecución parcial determinista y ramas XOR;
- los testigos negativos no alcanzan la ruta;
- no existen aristas huérfanas o duplicadas.

### Desenlace primario

Tasa de testigos que ejecutan exactamente la variante asignada. Para restricciones
duras de la demo se exige 100 %. Una sola violación bloquea la arista.

## Fase 3. Validez clínica de contenido

### Panel

Panel independiente con:

- especialistas en obstetricia y medicina materno-fetal;
- experiencia con la GPC o el contexto asistencial;
- una persona de metodología o epidemiología;
- manejo declarado de conflictos de interés.

El tamaño y el umbral se fijan antes de analizar. Como referencia metodológica,
un panel de 6 a 10 especialistas permite usar I-CVI, pero la decisión final debe
considerar el número exacto y la probabilidad de acuerdo por azar.

### Cegamiento

Los revisores reciben IDs y evidencia fuente, pero no el resultado de matching
ni la decisión de otros revisores. Se aleatoriza el orden de unidades.

### Dominios, escala 1 a 4

1. fidelidad de la ruta a la GPC;
2. suficiencia de variables;
3. coherencia de restricciones;
4. validez del testigo;
5. corrección de la acción terminal;
6. trazabilidad;
7. riesgo de interpretación clínica incorrecta.

Puntuaciones 1-2 significan revisión mayor; 3-4, aceptación de contenido con o
sin ajuste menor. Toda puntuación 1-2 requiere justificación.

### Indicadores

\[
I\text{-}CVI_i=
\frac{\#\text{revisores que puntúan 3 o 4}}
{\#\text{respuestas válidas}}.
\]

\[
S\text{-}CVI/Ave=\operatorname{media}(I\text{-}CVI_i).
\]

Se reportan además:

- distribución completa;
- acuerdo porcentual;
- kappa modificado si el tamaño lo permite;
- comentarios y causas;
- cambios entre rondas;
- pares rechazados y no solo los aprobados.

Un promedio global alto no rescata una restricción clínicamente crítica.

### Adjudicación

Las unidades bajo umbral regresan al LOOP:

    observación → fuente → regla → testigo → nueva revisión

No se eliminan ni corrigen silenciosamente.

## Fase 4. Evaluación de assignment_manifest.json

Se comprueba:

- cardinalidad óptima;
- unicidad de IDs;
- testigo y hash por par;
- explicación de variantes libres;
- ausencia de prioridad clínica implícita;
- posibilidad de reproducir cada asignación.

### Comparación exploratoria futura

Comparar generación directa contra generación guiada por
**assignment_manifest.json**:

- misma GPC y mismo número de intentos;
- misma tecnología generativa;
- semillas y parámetros registrados;
- evaluación clínica cegada;
- desenlace primario: proporción que ejecuta la ruta solicitada sin violaciones.

La hipótesis es que la capa previa reduce fallos lógicos y omisiones. No se
declara confirmada en esta entrega.

## Fase 5. Validación generativa

Solo comienza cuando existan instancias o registros sintéticos.

### Fidelidad lógica

- tasa de ejecución de ruta;
- violaciones de condiciones obligatorias;
- presencia de combinaciones prohibidas;
- coherencia de estado inicial y terminal.

### Fidelidad estadística

- distribuciones marginales;
- asociaciones y coocurrencias;
- temporalidad;
- prevalencia de rutas según una fuente externa válida;
- análisis de subgrupos.

### Diversidad

- duplicados exactos y aproximados;
- concentración por estructura;
- cobertura de dominios permitidos;
- entropía o soporte efectivo cuando sea apropiado.

### Consistencia clínica

- revisión cegada por especialistas;
- errores de medicación, temporalidad o causalidad;
- severidad y accionabilidad de cada error;
- acuerdo interevaluador.

### Utilidad

Se define por el uso previsto. Para modelos predictivos puede emplearse
Train-on-Synthetic, Test-on-Real, con un conjunto real retenido y no usado por
el generador. No existe una métrica universal de utilidad.

### Privacidad

Si el generador aprende de registros reales:

- membership inference;
- attribute inference;
- nearest-neighbor disclosure;
- memorization;
- evaluación por subgrupos.

La etiqueta “sintético” no garantiza privacidad.

## Fase 6. Replicación

Aplicar el protocolo a una segunda GPC sin mezclar fuentes:

- construir \(D_2\), \(U_2\), \(V_2\) y \(B_2\);
- medir porcentaje de rutas con estructura;
- comparar densidad y déficit;
- registrar reglas nuevas;
- evaluar estabilidad de decisiones expertas.

Esto estudia transportabilidad, no validez clínica universal.

## Criterios de reporte

Publicar:

- protocolo y desviaciones;
- versiones y hashes;
- diccionario de variables;
- reglas de inclusión y exclusión;
- todos los resultados algorítmicos;
- calificaciones anonimizadas cuando sea éticamente posible;
- resultados generativos favorables y desfavorables;
- limitaciones y conflictos de interés.
