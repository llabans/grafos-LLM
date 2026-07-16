# Protocolo prospectivo de validación

## Objetivo

Evaluar de forma separada:

1. la validez clínica de contenido de los escenarios y sus vínculos;
2. la validez educativa de los microobjetivos;
3. la utilidad del matching como herramienta de curación de un banco de casos.

El protocolo no busca validar un sistema de soporte a decisiones clínicas.

## Fase 0 — registro y congelamiento

Antes de recibir calificaciones:

- congelar la versión de la GPC, reglas, grafo y formulario;
- registrar hipótesis, desenlaces y umbrales;
- asignar IDs ciegos a casos y objetivos;
- separar desarrolladores de revisores;
- conservar todas las respuestas, incluidas las discordantes.

## Fase 1 — panel de contenido

### Participantes

Panel independiente con diversidad de roles:

- especialistas clínicos en obstetricia;
- profesionales con experiencia en educación médica;
- una persona con experiencia metodológica o epidemiológica.

El número final debe justificarse antes de analizar datos. No se rellenarán
calificaciones faltantes ni se sustituirán revisores después de observar los
resultados.

### Unidades evaluadas

- siete escenarios simbólicos;
- ocho microobjetivos;
- catorce aristas caso-objetivo;
- una muestra de pares rechazados para evaluar especificidad de la regla.

### Escala

Cada unidad se califica de 1 a 4:

1. no pertinente/inadecuada;
2. requiere revisión mayor;
3. pertinente con revisión menor;
4. pertinente y clara.

Dominios:

- fidelidad a la GPC;
- coherencia clínica;
- relevancia educativa;
- claridad;
- suficiencia de la compatibilidad.

Se añade una respuesta binaria independiente: “¿aprobaría esta arista?” y un
campo obligatorio de justificación cuando la respuesta sea no.

### Indicadores

Para cada unidad y dominio:

\[
I\text{-}CVI=\frac{\#\text{revisores con puntuación 3 o 4}}
{\#\text{revisores con respuesta válida}}.
\]

El índice global será:

\[
S\text{-}CVI/Ave=\operatorname{media}(I\text{-}CVI_i).
\]

Se reportarán también distribución completa, acuerdo porcentual, comentarios y
decisiones de revisión. Los umbrales se preespecificarán según el tamaño del
panel y no se modificarán tras observar los datos. La metodología se apoya en
Polit, Beck y Owen (2007), DOI `10.1002/nur.20199`.

### Gate

Un caso o arista que no alcance el umbral preespecificado se revisa y regresa a
una segunda ronda. No se elimina silenciosamente. El historial de cambios debe
mostrar qué fuente y qué regla se modificaron.

## Fase 2 — estudio de utilidad para autoría

### Diseño propuesto

Estudio cruzado con docentes o autores de casos:

- condición A: selección manual con lista estructurada;
- condición B: selección asistida por grafo y matching;
- orden contrabalanceado;
- mismos objetivos y tiempo máximo;
- evaluación final cegada al método cuando sea posible.

### Desenlace primario

Número de microobjetivos distintos con un representante compatible y distinto.

### Desenlaces secundarios

- redundancia del banco;
- tiempo de construcción;
- número de vínculos rechazados por expertos;
- carga percibida y usabilidad;
- comprensión de la brecha `8>7`.

La muestra se calculará a partir de un piloto o de un efecto mínimo relevante
definido antes de la prueba principal. No se escogerá `n` por conveniencia para
obtener significación.

## Fase 3 — piloto educativo

Solo después de aprobar la fase de contenido:

- población y nivel formativo claramente definidos;
- objetivos observables y evaluación alineada;
- comparación pre/post o grupo comparador según factibilidad;
- análisis de dificultad, discriminación y errores por objetivo;
- registro de eventos o contenidos potencialmente inseguros;
- conclusión limitada al contexto y cohorte estudiados.

La cobertura del grafo es un atributo del banco; el aprendizaje es un desenlace
del estudiante. Deben analizarse por separado.

## Fase 4 — replicación estructural

Como trabajo futuro, aplicar las mismas reglas a una segunda GPC sin mezclarlas
en un solo grafo. Construir `B1` y `B2` y comparar:

- proporción de entidades trazables;
- densidad;
- déficit de Hall;
- estabilidad de decisiones expertas;
- cambios requeridos en las reglas.

Esta fase evalúa transportabilidad del método, no validez clínica universal.

## Flujo LOOP con gates

```text
CONGELAR
  ↓ gate de fuente
CONSTRUIR
  ↓ gate algorítmico
REVISAR POR EXPERTOS
  ↓ gate de contenido
PILOTAR CON AUTORES/ESTUDIANTES
  ↓ gate educativo
REPLICAR
  ↺ actualizar reglas con historial explícito
```

## Transparencia

Publicar:

- formulario y diccionario de variables;
- reglas de exclusión;
- análisis planeado;
- datos anonimizados de calificaciones cuando el consentimiento lo permita;
- todos los resultados, no solo los favorables;
- versión exacta de código, GPC y artefactos.
