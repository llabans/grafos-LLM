# Metodología para la construcción de un grafo multicapa de una guía de práctica clínica y su uso como conocimiento estructurado para fine-tuning

## 1. Propósito metodológico

La presente metodología propone transformar una guía de práctica clínica (GPC) en un **grafo de conocimiento dirigido, multicapa y trazable**, y utilizar sus subgrafos como unidades semánticas de conocimiento para el ajuste fino de un modelo de lenguaje.

El objetivo no es generar casos clínicos sintéticos ni convertir la guía en una colección convencional de preguntas y respuestas. El propósito es preservar, dentro de cada unidad de entrenamiento, la estructura explícita de la guía: población, condiciones de aplicabilidad, reglas de decisión, acciones recomendadas, evidencia, justificación, metodología, contexto y procedencia documental.

La propuesta distingue dos conceptos:

1. **Unidad semántica de entrenamiento:** subgrafo autocontenido, coherente y trazable que representa cualquier unidad de conocimiento contenida en la guía de práctica clínica. Puede corresponder a una recomendación, una pregunta clínica, una definición, una regla de decisión, un algoritmo asistencial, una justificación, un cuerpo de evidencia, un componente metodológico, una consideración de implementación, una declaración de alcance o cualquier otra estructura documental o conceptual relevante.
2. **Representación computacional de entrada:** la forma en que dicho subgrafo se presenta al modelo, ya sea como una serialización textual reversible o mediante un codificador de grafos y un proyector hacia el espacio de embeddings del LLM.

Las recomendaciones pueden funcionar como nodos de anclaje frecuentes para construir subgrafos clínicos, pero no constituyen la única fuente ni el único tipo de conocimiento empleado en el entrenamiento. El corpus de fine-tuning deberá cubrir sistemáticamente todas las capas del grafo y, en conjunto, representar la totalidad del conocimiento explícito contenido en la guía.

Esta distinción es necesaria porque un modelo de lenguaje autorregresivo no puede consumir directamente una instancia de Neo4j como objeto nativo. La literatura emplea principalmente dos familias de soluciones: a) verbalización o serialización estructurada del grafo, y b) codificación del grafo mediante un encoder y alineación con el espacio de embeddings del LLM.

---

## 2. Diseño general

La metodología se organiza en ocho fases:

1. Delimitación y segmentación documental de la guía.
2. Definición del esquema semántico y de las capas del grafo.
3. Construcción de un subgrafo dirigido por recomendación.
4. Integración de los subgrafos en un grafo multicapa global.
5. Validación semántica, lógica, documental y estructural.
6. Extracción de unidades de conocimiento para entrenamiento.
7. Representación del grafo para fine-tuning.
8. Ajuste fino y evaluación del aprendizaje clínico, estructural y documental.

---

## 3. Fase 1. Delimitación y segmentación de la guía

### 3.1. Definición del alcance

Se registra la guía como una entidad documental principal y se explicita su alcance:

- problema o condición clínica abordada;
- población objetivo;
- nivel o contexto asistencial;
- intervenciones incluidas;
- desenlaces considerados;
- exclusiones expresas;
- aspectos que la guía no aborda.

El alcance debe representarse antes de ejecutar cualquier búsqueda de recomendaciones. En el algoritmo de consulta, la comprobación del alcance funciona como una puerta lógica: si una consulta está fuera de lo cubierto por la guía, el sistema debe informarlo y no inferir una recomendación inexistente.

### 3.2. Unidades documentales

La guía se segmenta conservando su estructura editorial y sus coordenadas de procedencia. Cada fragmento recibe un identificador persistente y metadatos como:

- documento y versión;
- capítulo y sección;
- página;
- párrafo;
- tabla, figura, algoritmo o flujograma;
- identificador de recomendación;
- pregunta clínica relacionada;
- referencias bibliográficas citadas.

No se elimina el texto narrativo. Los fragmentos se mantienen como nodos documentales enlazados con los conceptos clínicos y metodológicos que sustentan.

---

## 4. Fase 2. Esquema semántico del grafo multicapa

El grafo se define como dirigido, tipado, atribuido y multicapa. Las capas no son bases de datos independientes, sino agrupaciones semánticas dentro del mismo grafo.

### 4.1. Capa de alcance

Representa qué cubre y qué no cubre la guía.

**Nodos principales:**

- `Guia`
- `Alcance`
- `PoblacionObjetivo`
- `ProblemaClinico`
- `ContextoAsistencial`
- `Exclusion`
- `TemaNoAbordado`

**Relaciones de ejemplo:**

- `GUIA_TIENE_ALCANCE`
- `ALCANCE_INCLUYE_POBLACION`
- `ALCANCE_CUBRE_TEMA`
- `ALCANCE_EXCLUYE`
- `GUIA_NO_ABORDA`

La relación `GUIA_NO_ABORDA` solo debe utilizarse cuando la ausencia sea explícita o haya sido verificada sistemáticamente. No debe confundirse “no encontrado” con “expresamente no abordado”.

### 4.2. Capa clínica y decisional

Representa para quién aplica una recomendación, qué condiciones deben cumplirse y qué acción se propone.

**Nodos principales:**

- `PreguntaClinica`
- `Recomendacion`
- `Condicion`
- `ReglaDecision`
- `Intervencion`
- `Comparador`
- `Desenlace`
- `Frecuencia`
- `Temporalidad`
- `ExcepcionClinica`

**Relaciones de ejemplo:**

- `GUIA_CONTIENE_PREGUNTA`
- `PREGUNTA_TIENE_RECOMENDACION`
- `REGLA_EVALUA_CONDICION`
- `CONDICION_FORMA_PARTE_DE_REGLA`
- `REGLA_ACTIVA_RECOMENDACION`
- `RECOMENDACION_INDICA_INTERVENCION`
- `RECOMENDACION_TIENE_FRECUENCIA`
- `RECOMENDACION_CONSIDERA_DESENLACE`
- `REGLA_TIENE_EXCEPCION`

Una **condición** representa un predicado elemental, por ejemplo: sexo femenino, edad entre 40 y 69 años, ausencia de síntomas o riesgo bajo. Una **regla** combina condiciones mediante operadores lógicos y determina si una recomendación resulta aplicable.

Ejemplo abstracto:

```text
SI sexo = femenino
Y edad >= 40
Y edad <= 69
Y estado_sintomatico = asintomatica
Y nivel_riesgo = bajo
ENTONCES aplica Recomendacion_R1
```

### 4.3. Capa de evidencia y justificación

Representa por qué se formuló una recomendación.

**Nodos principales:**

- `Justificacion`
- `CuerpoEvidencia`
- `Estudio`
- `Beneficio`
- `RiesgoODano`
- `CertezaEvidencia`
- `BalanceBeneficioRiesgo`
- `ValoresPreferencias`
- `UsoRecursos`
- `Equidad`
- `Aceptabilidad`
- `Factibilidad`

**Relaciones de ejemplo:**

- `RECOMENDACION_TIENE_JUSTIFICACION`
- `JUSTIFICACION_SE_APOYA_EN_EVIDENCIA`
- `EVIDENCIA_REPORTA_BENEFICIO`
- `EVIDENCIA_REPORTA_DANO`
- `EVIDENCIA_TIENE_CERTEZA`
- `RECOMENDACION_CONSIDERA_BALANCE`
- `RECOMENDACION_CONSIDERA_FACTIBILIDAD`

La justificación científica no debe reducirse a un bloque de texto. Cuando la guía lo permita, debe descomponerse en componentes distinguibles, manteniendo también el fragmento narrativo original para preservar contexto.

### 4.4. Capa metodológica

Representa cómo se construyó la recomendación.

**Nodos principales:**

- `MetodoDesarrollo`
- `MarcoGRADE`
- `PreguntaPICO`
- `BusquedaEvidencia`
- `EvaluacionCalidad`
- `PanelExpertos`
- `ProcesoConsenso`
- `DeclaracionConflictoInteres`

**Relaciones de ejemplo:**

- `GUIA_UTILIZA_METODO`
- `PREGUNTA_SE_FORMULA_COMO_PICO`
- `EVIDENCIA_FUE_EVALUADA_MEDIANTE`
- `RECOMENDACION_FUE_FORMULADA_POR`
- `PANEL_APLICA_PROCESO_CONSENSO`

Esta capa responde preguntas como “¿cómo se elaboró la recomendación?” y no preguntas de aplicabilidad clínica.

### 4.5. Capa documental y de procedencia

Representa el origen exacto de cada afirmación.

**Nodos principales:**

- `Documento`
- `VersionDocumento`
- `Seccion`
- `Pagina`
- `Parrafo`
- `Tabla`
- `Figura`
- `Flujograma`
- `ReferenciaBibliografica`
- `FragmentoTexto`

**Relaciones de ejemplo:**

- `AFIRMACION_PROVIENE_DE_FRAGMENTO`
- `FRAGMENTO_PERTENECE_A_SECCION`
- `FRAGMENTO_ESTA_EN_PAGINA`
- `FRAGMENTO_APARECE_EN_TABLA`
- `FRAGMENTO_CITA_REFERENCIA`
- `DOCUMENTO_TIENE_VERSION`

Esta capa permite recuperar el texto que justifica una respuesta y su localización precisa.

### 4.6. Capa de contexto de implementación

Se incorpora solo cuando la guía contiene información relevante sobre el contexto asistencial.

**Nodos posibles:**

- `NivelAtencion`
- `DisponibilidadTecnologia`
- `RecursoDiagnostico`
- `CapacidadServicio`
- `BarrerasImplementacion`
- `EntornoAtencion`

No deben añadirse atributos como ruralidad, vulnerabilidad o disponibilidad tecnológica si no se encuentran explícita o justificadamente en la guía.

---

## 5. Fase 3. Construcción modular de subgrafos por unidad de conocimiento

La guía se modela mediante subgrafos modulares centrados en diferentes unidades de conocimiento. Las recomendaciones constituyen uno de los principales puntos de anclaje para los subgrafos clínicos, pero también se construyen subgrafos independientes para el alcance, las definiciones, los algoritmos, la evidencia, la metodología, la implementación y la procedencia documental. Este procedimiento evita intentar representar toda la guía de una sola vez y facilita la revisión experta por dominios.

### 5.1. Unidades mínimas de modelado

No se define una única unidad mínima universal. La unidad depende del tipo de conocimiento representado. Entre las principales configuraciones se incluyen:

```text
Subgrafo clínico-decisional
PreguntaClinica
    -> Recomendacion
    -> ReglaDecision
    -> Condiciones
    -> Intervencion
    -> Desenlaces
```

```text
Subgrafo científico
Recomendacion
    -> Justificacion
    -> CuerpoEvidencia
    -> Beneficios
    -> Danos
    -> CertezaEvidencia
```

```text
Subgrafo metodológico
PreguntaClinica
    -> PreguntaPICO
    -> BusquedaEvidencia
    -> EvaluacionCalidad
    -> MarcoGRADE
    -> ProcesoConsenso
```

```text
Subgrafo de alcance
Guia
    -> Alcance
    -> PoblacionObjetivo
    -> TemasCubiertos
    -> Exclusiones
    -> TemasNoAbordados
```

```text
Subgrafo documental
Afirmacion
    -> FragmentoTexto
    -> Seccion
    -> Pagina
    -> TablaOFigura
    -> ReferenciaBibliografica
```

La recomendación puede funcionar como **nodo bisagra** entre las capas clínica, probatoria, metodológica y documental, pero no todos los subgrafos necesitan estar centrados en una recomendación.

### 5.2. Procedimiento de construcción

Para cada unidad de conocimiento identificada en la guía:

1. Identificar el tipo de conocimiento representado.
2. Conservar el texto literal o fragmento documental correspondiente.
3. Identificar las entidades, propiedades y relaciones explícitas.
4. Formalizar reglas, condiciones u operadores lógicos cuando existan.
5. Registrar definiciones, acciones, intervenciones, frecuencias, temporalidades o desenlaces cuando correspondan.
6. Registrar excepciones, contraindicaciones, exclusiones, incertidumbres o temas no abordados.
7. Descomponer la justificación en beneficios, daños, certeza y otros criterios cuando la guía los proporcione.
8. Enlazar la evidencia, la metodología, las consideraciones de implementación y el contexto pertinente.
9. Registrar la procedencia documental exacta.
10. Someter el subgrafo a revisión experta según su dominio: clínica, metodológica, documental o de implementación.

### 5.3. Ejemplo conceptual

```text
(Guia)-[:CONTIENE_PREGUNTA]->(Pregunta_P1)
(Pregunta_P1)-[:TIENE_RECOMENDACION]->(Recomendacion_R1)

(Regla_RD1)-[:EVALUA]->(Condicion_SexoFemenino)
(Regla_RD1)-[:EVALUA]->(Condicion_Edad40_69)
(Regla_RD1)-[:EVALUA]->(Condicion_Asintomatica)
(Regla_RD1)-[:EVALUA]->(Condicion_RiesgoBajo)
(Regla_RD1)-[:ACTIVA]->(Recomendacion_R1)

(Recomendacion_R1)-[:INDICA]->(Intervencion_ExamenClinicoMama)
(Recomendacion_R1)-[:TIENE_FRECUENCIA]->(CadaDosAnios)
(Recomendacion_R1)-[:TIENE_JUSTIFICACION]->(Justificacion_J1)
(Justificacion_J1)-[:SE_APOYA_EN]->(Evidencia_E1)
(Recomendacion_R1)-[:PROVIENE_DE]->(Fragmento_F1)
(Fragmento_F1)-[:ESTA_EN]->(Pagina_Px)
```

El ejemplo es ilustrativo; los contenidos definitivos deben copiarse y formalizarse a partir de la recomendación real de la guía.

---

## 6. Fase 4. Integración de los subgrafos

Una vez validados individualmente, los subgrafos se integran en un grafo global.

### 6.1. Resolución de entidades

Se identifican nodos semánticamente equivalentes y se decide si deben fusionarse o mantenerse separados. Por ejemplo, “mujer”, “sexo femenino” y “paciente femenina” podrían corresponder al mismo concepto normalizado, pero sus menciones documentales deben conservarse.

Cada entidad puede contener:

- identificador interno estable;
- etiqueta preferida;
- sinónimos;
- definición operacional;
- tipo semántico;
- código terminológico, cuando sea pertinente;
- fuente y versión.

### 6.2. Reutilización controlada

Los conceptos clínicos comunes pueden compartirse entre recomendaciones. Sin embargo, no deben fusionarse reglas, justificaciones o fragmentos documentales únicamente por similitud textual. La procedencia y el contexto de cada recomendación deben mantenerse.

### 6.3. Restricciones de integridad

El esquema debe incluir restricciones como:

- toda recomendación pertenece a una pregunta clínica;
- toda recomendación posee al menos una referencia documental;
- toda regla de decisión se conecta con una o más condiciones;
- toda condición utilizada en una regla tiene tipo, operador y valor o rango;
- toda relación de evidencia conserva su fuente;
- una recomendación no puede simultáneamente indicar y contraindicar la misma intervención bajo idénticas condiciones, salvo que el documento explicite una incertidumbre o conflicto.

---

## 7. Fase 5. Validación del grafo

La validación no constituye una capa de la guía, sino un proceso metodológico aplicado al grafo construido.

### 7.1. Validación documental

Comprueba que cada nodo y relación pueda rastrearse a un fragmento de la guía. Se verifica:

- fidelidad del texto;
- página y sección correctas;
- correspondencia con tablas y flujogramas;
- versión documental;
- ausencia de información añadida sin fuente.

### 7.2. Validación semántica

Especialistas revisan que los conceptos y relaciones representen adecuadamente el significado clínico y metodológico.

### 7.3. Validación lógica

Se evalúan las reglas mediante casos de prueba mínimos, positivos, negativos y de frontera. Por ejemplo:

- edad mínima incluida;
- edad máxima incluida;
- edad inmediatamente fuera del rango;
- ausencia de una condición obligatoria;
- presencia de una exclusión;
- combinaciones contradictorias.

### 7.4. Validación estructural

Se aplican controles automáticos sobre:

- nodos huérfanos;
- relaciones inválidas;
- ciclos no permitidos en rutas decisionales;
- duplicados;
- propiedades obligatorias ausentes;
- cardinalidades;
- conectividad entre capas.

### 7.5. Validación interevaluador

Una muestra de recomendaciones debe ser modelada o revisada por al menos dos evaluadores. Se documentan los desacuerdos y las reglas de adjudicación. La concordancia puede evaluarse por tipo de nodo, relación, condición, operador lógico y procedencia.

---

## 8. Fase 6. Definición de la unidad de conocimiento para fine-tuning

### 8.1. El subgrafo como unidad semántica general

Cada ejemplo de entrenamiento corresponde a un **subgrafo autocontenido, coherente y trazable**, no a un caso sintético. El subgrafo puede representar cualquier unidad de conocimiento explícitamente contenida en la guía, incluyendo:

- alcance y objetivos;
- población objetivo y exclusiones;
- preguntas clínicas;
- recomendaciones;
- definiciones y conceptos;
- reglas de decisión;
- algoritmos y rutas asistenciales;
- intervenciones, comparadores y desenlaces;
- justificaciones;
- evidencia científica;
- beneficios, daños y certeza de evidencia;
- metodología de elaboración;
- preguntas PICO;
- procesos GRADE o Evidence-to-Decision;
- valores y preferencias;
- uso de recursos;
- equidad, aceptabilidad, factibilidad e implementación;
- tablas, figuras y flujogramas;
- referencias y procedencia documental;
- vacíos, incertidumbres y temas no abordados.

El subgrafo debe incluir todos los nodos necesarios para interpretar la unidad de conocimiento seleccionada y sus relaciones relevantes, pero excluir nodos ajenos que incrementen el contexto sin aportar significado. La totalidad del corpus debe proporcionar cobertura sistemática de todas las capas del grafo y no concentrarse únicamente en las recomendaciones.

### 8.2. Muestreo de subgrafos

Se propone un muestreo estratificado basado en tipos de conocimiento y plantillas estructurales:

- **Subgrafo de alcance:** guía → alcance → población → temas cubiertos/excluidos.
- **Subgrafo conceptual:** definición → concepto → sinónimos → relaciones semánticas.
- **Subgrafo clínico-decisional:** condiciones → regla → recomendación → intervención.
- **Subgrafo algorítmico:** estado clínico → decisión → acción → siguiente estado.
- **Subgrafo científico:** recomendación o pregunta → evidencia → beneficios/daños → certeza.
- **Subgrafo metodológico:** pregunta PICO → búsqueda → evaluación → GRADE → consenso.
- **Subgrafo de implementación:** recomendación → recursos/equidad/aceptabilidad/factibilidad.
- **Subgrafo documental:** afirmación → fragmento → página/sección/tabla/figura/referencia.
- **Subgrafo de incertidumbre:** afirmación → limitación → vacío de evidencia → tema no abordado.
- **Subgrafo multicapa completo:** integración controlada de varias rutas anteriores.

No se crean hechos clínicos nuevos. El muestreo selecciona rutas o vecindarios existentes dentro del grafo validado.

### 8.3. División experimental sin fuga de información

La separación entre entrenamiento, validación y prueba debe realizarse por unidades semánticas superiores, no por líneas serializadas. Algunas opciones son:

- separar por recomendación;
- separar por pregunta clínica;
- separar por familia de intervención;
- separar por secciones de la guía.

Una misma recomendación no debe aparecer parcialmente en entrenamiento y parcialmente en prueba, porque produciría fuga estructural y documental.

---

## 9. Fase 7. Representación del grafo para fine-tuning

La literatura revisada muestra que “entrenar directamente con grafos” requiere definir una interfaz entre la estructura gráfica y el LLM. Se identifican tres estrategias.

### 9.1. Estrategia A: serialización textual estructurada

El subgrafo se convierte, de manera determinista y reversible, en una secuencia de tokens. InstructGraph utiliza un verbalizador de formato estructurado parecido a código; GraphText transforma el grafo en un árbol sintáctico y luego en una secuencia textual; estudios comparativos han encontrado que JSON puede superar a descripciones en lenguaje natural y formatos de código en diversas tareas de instrucción sobre grafos.

Ejemplo:

```json
{
  "graph_id": "R1_decision",
  "center": "Recomendacion_R1",
  "nodes": [
    {"id": "C1", "type": "Condicion", "predicate": "sexo", "operator": "=", "value": "femenino"},
    {"id": "C2", "type": "Condicion", "predicate": "edad", "operator": "between", "value": [40, 69]},
    {"id": "RD1", "type": "ReglaDecision", "logic": "C1 AND C2 AND C3 AND C4"},
    {"id": "R1", "type": "Recomendacion", "text": "..."}
  ],
  "edges": [
    {"source": "RD1", "relation": "EVALUA", "target": "C1"},
    {"source": "RD1", "relation": "EVALUA", "target": "C2"},
    {"source": "RD1", "relation": "ACTIVA", "target": "R1"}
  ],
  "provenance": {
    "document": "...",
    "page": "...",
    "section": "..."
  }
}
```

**Ventajas:**

- compatible con Qwen y herramientas estándar de LoRA/QLoRA;
- no exige modificar la arquitectura del modelo;
- facilita auditoría y reproducción;
- conserva identificadores, tipos y direcciones;
- permite entrenar con subgrafos sin generar casos sintéticos.

**Limitaciones:**

- la estructura queda mediada por una secuencia lineal;
- el orden de serialización puede influir en el aprendizaje;
- los subgrafos grandes pueden exceder el contexto;
- el modelo puede memorizar cadenas sin aprender invariancia estructural.

### 9.2. Estrategia B: encoder de grafos y proyector hacia el LLM

GraphGPT, LLaGA, GraphLLM y trabajos relacionados utilizan un encoder gráfico o representaciones estructurales y un proyector entrenable para alinear esas representaciones con el espacio de embeddings del LLM. En este enfoque, el subgrafo no se reduce enteramente a texto: se codifica como vectores estructurales que se insertan como tokens gráficos o prefijos continuos.

Flujo conceptual:

```text
Subgrafo -> encoder de grafos/GNN -> embeddings estructurales
         -> proyector -> espacio de embeddings de Qwen
         -> capas del LLM -> respuesta
```

**Ventajas:**

- preserva mejor la topología;
- puede aprender invariancias al orden de presentación;
- separa atributos textuales y estructura relacional;
- constituye una aproximación más cercana al uso nativo del grafo.

**Limitaciones:**

- requiere desarrollo arquitectónico adicional;
- necesita adaptar el pipeline de entrenamiento;
- aumenta la complejidad experimental y de depuración;
- puede ser difícil de ejecutar con recursos limitados;
- exige definir cómo se codifican nodos clínicos, relaciones tipadas y textos largos.

### 9.3. Estrategia C: enfoque híbrido

El enfoque híbrido combina:

1. serialización estructurada del subgrafo para el fine-tuning del LLM;
2. acceso al grafo original durante inferencia para verificación y trazabilidad;
3. eventualmente, un encoder/proyector gráfico como experimento comparativo.

Esta alternativa permite que el modelo aprenda patrones decisionales y semánticos, pero mantiene al grafo como fuente externa verificable. En aplicaciones clínicas, el fine-tuning no debe considerarse sustituto del grafo: los pesos pueden quedar desactualizados, omitir excepciones o producir respuestas no fieles. El acceso al grafo conserva la procedencia y posibilita comprobar cada recomendación.

---

## 10. Estrategia recomendada para el estudio

Para un modelo Qwen 3.5 de aproximadamente 9B parámetros y recursos locales, se recomienda utilizar la **Estrategia A como experimento principal** y la **Estrategia C como arquitectura final**.

### 10.1. Justificación

- Es compatible con fine-tuning eficiente mediante LoRA o QLoRA.
- No requiere construir inicialmente una GNN ni modificar el núcleo de Qwen.
- Mantiene el subgrafo como unidad semántica completa.
- Permite comparar diferentes serializaciones.
- Facilita demostrar trazabilidad entre entrada, salida y fragmento original.
- Evita introducir casos clínicos artificiales que no estén contenidos en la guía.

### 10.2. Formatos a comparar

Se propone comparar al menos tres representaciones del mismo subgrafo:

1. **JSON tipado**, con listas explícitas de nodos, relaciones y procedencia.
2. **Tripletas ordenadas**, con encabezado de contexto y reglas formalizadas.
3. **Lenguaje controlado**, con sintaxis fija para condiciones, reglas, acciones y evidencia.

Ejemplo de tripletas:

```text
[GRAPH R1]
(C1:Condicion)-[PREDICADO]->(sexo=femenino)
(C2:Condicion)-[PREDICADO]->(edad BETWEEN 40 AND 69)
(RD1:Regla)-[EVALUA]->(C1)
(RD1:Regla)-[EVALUA]->(C2)
(RD1:Regla)-[ACTIVA]->(R1:Recomendacion)
(R1)-[PROVIENE_DE]->(F1:Fragmento)
[/GRAPH]
```

El formato seleccionado debe ser estable, no ambiguo, reversible y capaz de distinguir tipos de nodo, dirección de relaciones, propiedades, operadores lógicos y procedencia.

---

## 11. Fase 8. Fine-tuning basado en subgrafos

### 11.1. Objetivo de aprendizaje

El fine-tuning busca que el modelo aprenda a:

- interpretar una estructura de grafo clínico;
- reconocer condiciones y operadores lógicos;
- determinar la aplicabilidad de una recomendación;
- recuperar la acción recomendada;
- explicar la justificación sin mezclarla con la regla clínica;
- identificar el origen documental;
- reconocer cuándo un tema está fuera del alcance de la guía;
- abstenerse cuando el grafo no contiene soporte suficiente.

### 11.2. Tareas de entrenamiento derivadas del mismo subgrafo

Aunque el subgrafo es la unidad de conocimiento, puede utilizarse con diferentes objetivos de salida, sin inventar contenido externo:

- reconstrucción parcial de nodos o relaciones ocultas;
- predicción de la relación correcta;
- identificación de la recomendación activada por una regla;
- explicación de una ruta decisional;
- recuperación de evidencia y procedencia;
- clasificación dentro/fuera del alcance;
- detección de contradicciones estructurales;
- conversión entre dos serializaciones equivalentes.

Estas tareas no constituyen casos clínicos sintéticos. Son transformaciones supervisadas del mismo conocimiento gráfico validado.

### 11.3. Función de pérdida

En la opción de serialización textual, se utiliza la pérdida autorregresiva habitual sobre los tokens de salida. Puede complementarse con:

- ponderación de tokens estructurales;
- pérdida auxiliar para tipos de relaciones;
- penalización de respuestas sin procedencia;
- entrenamiento por preferencias con ejemplos estructuralmente incorrectos.

### 11.4. Ajuste eficiente

Se recomienda:

- LoRA o QLoRA sobre el modelo base;
- congelar inicialmente la mayor parte de los parámetros;
- utilizar secuencias acotadas por subgrafo;
- aplicar acumulación de gradiente;
- controlar la proporción entre contenido clínico, evidencia, metodología y procedencia;
- conservar un conjunto de prueba compuesto por recomendaciones completas no vistas.

---

## 12. Evaluación

La evaluación debe separar el aprendizaje textual del aprendizaje de la estructura y la decisión clínica.

### 12.1. Fidelidad clínica

- exactitud de la recomendación recuperada;
- exactitud de aplicabilidad;
- sensibilidad ante exclusiones;
- desempeño en valores de frontera;
- tasa de recomendaciones inventadas.

### 12.2. Razonamiento estructural

- precisión de nodos y relaciones;
- exactitud de recorridos multi-salto;
- recuperación de condiciones necesarias y suficientes;
- robustez frente a cambios del orden de serialización;
- reconstrucción de subgrafos.

### 12.3. Trazabilidad

- exactitud de página, sección, tabla o fragmento;
- proporción de respuestas con procedencia válida;
- concordancia entre explicación y ruta del grafo;
- detección de soporte insuficiente.

### 12.4. Conocimiento no clínico

- reconocimiento del alcance;
- identificación de temas no abordados;
- recuperación de metodología y certeza de evidencia;
- diferenciación entre recomendación, justificación y referencia.

### 12.5. Comparaciones experimentales

Se propone comparar:

1. modelo base sin fine-tuning;
2. modelo ajustado con texto lineal de la guía;
3. modelo ajustado con subgrafos serializados;
4. modelo ajustado con subgrafos más consulta al grafo en inferencia;
5. opcionalmente, modelo con encoder/proyector gráfico.

La comparación 2 versus 3 permite estimar si la estructura explícita del grafo aporta beneficios frente al uso del texto documental sin estructurar.

---

## 13. Riesgos y controles

### 13.1. Memorización en lugar de razonamiento

Se controla mediante particiones por recomendación, alteración controlada del orden de nodos, pruebas de equivalencia estructural y evaluación con combinaciones lógicas no vistas pero sustentadas por reglas existentes.

### 13.2. Pérdida de estructura por serialización

Se utilizan identificadores estables, relaciones dirigidas explícitas, delimitadores, tipos semánticos, reglas formalizadas y pruebas de reconstrucción automática del grafo desde la secuencia.

### 13.3. Alucinación clínica

Se incorporan ejemplos negativos estructurales, respuestas de abstención y verificación contra el grafo durante inferencia.

### 13.4. Desactualización del conocimiento en pesos

El grafo se conserva como fuente versionada. Una nueva versión de la guía debe generar una nueva versión del grafo y un análisis de diferencias. El modelo ajustado debe declarar la versión aprendida y consultar el grafo actualizado para respuestas de alto riesgo.

### 13.5. Ambigüedad documental

Las decisiones de formalización deben registrarse en un log de curación con justificación, evaluador, fecha y fragmento fuente.

---

## 14. Producto final de la metodología

El resultado esperado es un sistema compuesto por:

1. un grafo de conocimiento dirigido y multicapa;
2. subgrafos validados para todas las unidades de conocimiento relevantes de la guía;
3. un esquema formal de nodos, relaciones y restricciones;
4. una representación reversible de cada subgrafo para entrenamiento;
5. un modelo Qwen ajustado para interpretar y explicar conocimiento gráfico;
6. un mecanismo de consulta al grafo para verificación y trazabilidad;
7. un protocolo de evaluación clínica, estructural, documental y metodológica.

El aporte no consiste únicamente en “pasar una guía a Neo4j”. Consiste en proponer y evaluar un procedimiento reproducible para convertir la totalidad del conocimiento explícito de una GPC en conocimiento gráfico computable, utilizar subgrafos heterogéneos como unidades semánticas de entrenamiento y mantener el grafo original como fuente verificable durante la inferencia.

---

## 15. Formulación metodológica resumida

> Se construirá un grafo de conocimiento dirigido y multicapa a partir de una guía de práctica clínica. La guía será descompuesta en subgrafos modulares que representarán no solo recomendaciones y preguntas clínicas, sino también definiciones, alcance, reglas de decisión, algoritmos, evidencia, justificaciones, metodología, consideraciones de implementación, incertidumbres y procedencia documental. Los subgrafos serán validados individualmente e integrados mediante resolución de entidades y reutilización controlada de conceptos. Para el ajuste fino del modelo de lenguaje, cada subgrafo constituirá una unidad semántica de conocimiento, y el conjunto total de unidades deberá representar sistemáticamente todas las capas de conocimiento contenidas en la guía. Debido a que el LLM opera sobre secuencias de tokens, los subgrafos serán transformados mediante una serialización estructurada, determinista y reversible que conserve los tipos de nodo, las relaciones dirigidas, los operadores lógicos y la procedencia. Se compararán diferentes formatos de representación y se evaluará si el entrenamiento basado en subgrafos mejora la interpretación de reglas clínicas, la recuperación de recomendaciones, la explicación de su fundamento, el reconocimiento del alcance y la trazabilidad documental, frente al entrenamiento basado únicamente en texto lineal. Durante la inferencia, el modelo podrá consultar el grafo original como mecanismo de verificación, con el fin de reducir alucinaciones y mantener la correspondencia con la versión vigente de la guía.

---

## Referencias seleccionadas

1. Tang, J., et al. (2023). **GraphGPT: Graph Instruction Tuning for Large Language Models**. arXiv:2310.13023.
2. Wang, J., et al. (2024). **InstructGraph: Boosting Large Language Models via Graph-centric Instruction Tuning and Preference Alignment**. arXiv:2402.08785.
3. Zhao, J., et al. (2023). **GraphText: Graph Reasoning in Text Space**. arXiv:2310.01089.
4. Zhu, K., et al. (2024). **Investigating Instruction Tuning Large Language Models on Graphs**. arXiv:2408.05457.
5. Chen, R., et al. (2024). **LLaGA: Large Language and Graph Assistant**. Proceedings of ICML 2024; arXiv:2402.08170.
6. Chai, Z., et al. (2023). **GraphLLM: Boosting Graph Reasoning Ability of Large Language Model**. arXiv:2310.05845.
7. Tan, Y., et al. (2024). **MuseGraph: Graph-oriented Instruction Tuning of Large Language Models for Generic Graph Mining**. arXiv:2403.04780.
8. Gao, Y., et al. (2023). **Leveraging a Medical Knowledge Graph into Large Language Models for Diagnosis Prediction**. arXiv:2308.14321.
9. Jia, M., et al. (2025). **Integrating Knowledge Graphs as Assistants of LLMs for Enhanced Clinical Diagnosis**. Proceedings of COLING 2025.
10. He, J., et al. (2025). **Evaluating and Improving Graph-to-Text Generation with Large Language Models**. arXiv:2501.14497.

## Nota sobre el estado de la evidencia

Los trabajos citados demuestran varias formas de alinear grafos y LLMs, pero la mayor parte de la evidencia se concentra en benchmarks generales de grafos, clasificación de nodos, razonamiento estructural o question answering. No existe todavía un consenso establecido para el fine-tuning de un LLM pequeño empleando subgrafos multicapa derivados de una única guía clínica como unidad semántica. Por ello, la selección del formato de serialización, el esquema de tareas y la evaluación de fidelidad clínica constituyen componentes experimentales centrales de la propuesta.
