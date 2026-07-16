# Revisión de literatura: guías clínicas, casos simulados y cobertura educativa

## Propósito y alcance

Esta revisión examina si existe soporte científico para representar la relación entre
casos clínicos simulados y blancos educativos derivados de una guía de práctica
clínica (GPC) mediante un grafo bipartito, y seleccionar el mayor número de
asignaciones uno-a-uno con emparejamiento máximo.

La revisión separa cuatro problemas que no deben confundirse:

1. Formalizar o volver computable una GPC narrativa.
2. Generar o curar pacientes virtuales y viñetas clínicas.
3. Planificar una colección que cubra contenidos u objetivos distintos.
4. Optimizar la asignación de materiales educativos bajo restricciones.

La fuente algorítmica principal del proyecto continúa siendo *Introduction to
Algorithms*, cuarta edición, de Cormen, Leiserson, Rivest y Stein (CLRS). El artículo
original de Hopcroft y Karp se utiliza como antecedente histórico del algoritmo y de
su cota, no como sustituto de CLRS para la exposición del curso.

## Método de búsqueda

**Fecha de la búsqueda:** 15 de julio de 2026, zona horaria America/Lima.

Se realizó un mapa dirigido de evidencia en PubMed, Crossref, OpenAlex, arXiv,
medRxiv y páginas de editoriales. Se usaron combinaciones de los siguientes términos:

- `clinical practice guideline`, `computer-interpretable guideline`, `GLIF`,
  `PROforma`, `guideline knowledge model`;
- `clinical vignette generation`, `virtual patient`, `medical simulation scenario`,
  `guideline-grounded`, `synthetic patient`;
- `learning objective`, `curriculum mapping`, `blueprint`, `case collection`,
  `coverage`;
- `bipartite matching`, `maximum matching`, `automated test assembly`,
  `binary programming`, `content constraints`.

Se incluyeron artículos originales, estudios de evaluación, proceedings, estándares
originales y preprints directamente relacionados con alguno de los cuatro problemas.
Las revisiones se usaron solo para localizar fuentes primarias y no como evidencia en
la matriz. Se excluyeron aplicaciones genéricas de preguntas y respuestas médicas,
grafos sin relación con diseño educativo y trabajos de diagnóstico que no abordaban
generación, curación o planificación de casos.

Este procedimiento no constituye una revisión sistemática registrada ni una búsqueda
exhaustiva de todas las bases bibliográficas e idiomas. Por ello, la ausencia de un
precedente exacto debe interpretarse como “no identificado en la búsqueda realizada”
y no como prueba de prioridad mundial.

## Matriz de evidencia primaria

| Fuente primaria | Tipo | Aporte para este proyecto | Cercanía al enfoque | Limitación frente al enfoque propuesto |
|---|---|---|---|---|
| Peleg et al. (2003), [*Comparing Computer-interpretable Guideline Models*](https://doi.org/10.1197/jamia.M1135) | Artículo revisado por pares | Comparó seis formalismos computables codificando fragmentos de dos GPC. Sustenta representar planes, decisiones, acciones, escenarios y datos de una guía mediante componentes explícitos. | Fundacional para GPC computables | No genera casos educativos ni optimiza su cobertura. |
| Boxwala et al. (2004), [*GLIF3*](https://doi.org/10.1016/j.jbi.2004.04.002) | Artículo revisado por pares | Propone niveles conceptual, computable e implementable y permite examinar consistencia y completitud lógica de la guía codificada. | Fundacional para trazabilidad estructural | Está orientado a soporte de decisión clínica, no a educación ni selección de casos. |
| Walonoski et al. (2018), [*Synthea*](https://doi.org/10.1093/jamia/ocx079) | Artículo revisado por pares | Usa estadísticas públicas, GPC y mapas asistenciales codificados como máquinas de estados para producir pacientes sintéticos. Demuestra que una GPC puede alimentar una representación generativa inspeccionable. | Alta para el enlace GPC→paciente sintético | No asigna casos a objetivos educativos. Su validación inicial halló errores clínico-estadísticos graves, lo que demuestra que estructura correcta no implica realismo clínico. |
| Deng et al. (2026), [*CPGPrompt*](https://arxiv.org/abs/2601.03475) | **Preprint** | Traduce GPC narrativas a árboles de decisión y evalúa su navegación con viñetas sintéticas en tres dominios. Reporta F1 de 0.85–1.00 en decisión binaria y 0.47–0.77 en clasificación multiclase. | Muy alta para GPC→estructura→viñeta | Las viñetas evalúan soporte de decisiones; no hay objetivos educativos, colección ni matching. |
| Mayer et al. (2022), [*Planning a Collection of Virtual Patients to Train Clinical Reasoning*](https://doi.org/10.3390/ijerph19106175) | Artículo revisado por pares | Construye un *blueprint* de 200 pacientes virtuales con criterios de enfermedad, paciente, encuentro y aprendiz; cubre 29 síntomas clave y 176 diagnósticos. Formaliza la cobertura a nivel de colección antes de escribir casos. | Muy alta para el problema de portafolio | La cobertura se resolvió mediante fuentes, consenso y refinamiento manual, sin GPC ni optimización combinatoria. |
| Fąferek et al. (2025), [*Applying ChatGPT to Plan and Create a Realistic Collection of Virtual Patients*](https://doi.org/10.1186/s12909-025-08006-9) | Artículo revisado por pares | Intentó generar un *blueprint* de 200 pacientes. El modelo omitió 13 síntomas solicitados, añadió 13 no solicitados y produjo patrones repetitivos y combinaciones atípicas. Después de revisión multietapa, cinco casos generados fueron comparables con cinco casos humanos. | Es el antecedente más cercano al problema de auditoría de cobertura | No usa una GPC ni un grafo. La evaluación final de casos no corrige por sí sola los defectos del *blueprint* completo. |
| Takahashi et al. (2024), [*Educational Utility of Clinical Vignettes Generated in Japanese by ChatGPT-4*](https://doi.org/10.2196/59133) | Artículo revisado por pares | Seleccionó 18 enfermedades desde un currículo oficial, una por área, y generó 18 viñetas. Setenta y un médicos calificaron calidad, exactitud, utilidad, realismo y dificultad. | Muy alta para fuente curricular→casos→validación experta | La selección fue estratificada manualmente; no deriva de una GPC ni usa optimización. La exactitud suficiente fue 67.9%, por lo que la generación no reemplaza la revisión clínica. |
| Bakkum et al. (2024), [*Using Artificial Intelligence to Create Diverse and Inclusive Medical Case Vignettes*](https://doi.org/10.1111/bcp.15977) | Artículo revisado por pares | Produjo conjuntos de 30 casos en aproximadamente 60 minutos mediante una secuencia reutilizable de prompts; muestra viabilidad y escalabilidad inicial. | Media-alta para generación de colecciones | Maximizar diversidad redujo representatividad. No hay GPC, compatibilidades explícitas ni cobertura optimizada. |
| Benoit (2023), [*ChatGPT for Clinical Vignette Generation, Revision, and Evaluation*](https://doi.org/10.1101/2023.02.04.23285478) | **Preprint medRxiv** | Evalúa generación y reescritura controlada. Al adaptar viñetas a baja alfabetización sanitaria se perdieron síntomas complejos en 87.5% de los casos. | Media para control de fidelidad | No estudia portafolios, GPC u objetivos; evidencia que una transformación textual puede perder atributos clínicos. |
| Sumpter (2024), [*Automated Generation of High-Quality Medical Simulation Scenarios*](https://arxiv.org/abs/2404.19713) | **Preprint** | Combina datos semiestructurados y un LLM para producir escenarios adaptados a objetivos educativos. | Alta en la idea de datos estructurados→escenario→objetivo | Evidencia empírica limitada; no documenta GPC trazable ni selección óptima del conjunto. |
| Liu (2025), [*Retrieval-Augmented Generation of Pediatric Speech-Language Pathology Vignettes*](https://arxiv.org/abs/2511.08600) | **Preprint** | Usa RAG y conocimiento curado para producir siete escenarios y evaluarlos en completitud, consistencia y adecuación clínica. | Alta para generación fundamentada | La evaluación es principalmente automática. El propio estudio declara pendientes revisión experta, piloto estudiantil y psicometría. |
| Gierl, Lai y Turner (2012), [*Using Automatic Item Generation to Create Multiple-choice Test Items*](https://doi.org/10.1111/j.1365-2923.2012.04289.x) | Artículo revisado por pares | Estructura contenido médico como modelo cognitivo→modelo de ítem→generación; produjo 1248 ítems desde un modelo de cirugía. | Media-alta como analogía de ingeniería educativa | Genera preguntas, no casos; no usa GPC ni audita un portafolio. |
| Gierl y Lai (2013), [*Evaluating the Quality of Medical Multiple-choice Items Created with Automated Processes*](https://doi.org/10.1111/medu.12202) | Estudio de evaluación revisado por pares | Cuatro expertos evaluaron 45 ítems. Los automáticos y manuales fueron comparables en siete de ocho indicadores, aunque los distractores automáticos fueron más débiles. | Alta para el diseño de validación de contenido | Valida ítems individuales, no cobertura de una colección ni fidelidad a una GPC. |
| Willett et al. (2008), [*It’s about TIME*](https://doi.org/10.1111/j.1365-2923.2008.03012.x) | Artículo revisado por pares | Desarrolla una taxonomía médica que vincula competencias, resultados, objetivos, temas, objetos de aprendizaje y preguntas. | Alta para definir el lado derecho del grafo | Advierte que mapear directamente a objetivos puede ser demasiado granular. No selecciona casos ni optimiza. |
| Theunissen (1985), [*Binary Programming and Test Design*](https://doi.org/10.1007/BF02296260) | Artículo revisado por pares | Introduce selección algorítmica de ítems mediante programación binaria. | Fundamento de optimización educativa | No es médico y emplea un modelo más general que matching. |
| van der Linden y Boekkooi-Timminga (1989), [*A Maximin Model for IRT-based Test Design with Practical Constraints*](https://doi.org/10.1007/BF02294518) | Artículo revisado por pares | Muestra que una prueba puede optimizarse bajo restricciones prácticas y de contenido expresadas linealmente. | Analogía matemática fuerte | Sugiere migrar a programación entera cuando existen pesos, cuotas o capacidades múltiples; no estudia pacientes virtuales. |
| Watts et al. (2021), [*Healthcare Simulation Standards of Best Practice: Simulation Design*](https://doi.org/10.1016/j.ecns.2021.08.009) | Estándar profesional original | Sustenta diseñar escenarios desde necesidades y objetivos explícitos, medibles y alineados con la actividad. | Alta para la semántica educativa | Es una norma de diseño, no una evaluación del matching. |
| Huwendiek et al. (2015), [instrumento para evaluar diseño de pacientes virtuales](https://doi.org/10.3109/0142159X.2014.970622) | Estudio de validación revisado por pares | Valida un instrumento de tres factores con 2547 evaluaciones de 78 pacientes virtuales; integra contenido, proceso de respuesta y estructura interna. | Alta para validación educativa | Estima que se necesitan cerca de 200 respuestas por paciente para una evaluación fiable en los tres factores, fuera del alcance usual de un curso. |
| Hicke et al. (2026), [*MedSimAI*](https://doi.org/10.1145/3785022.3785092) | Proceedings revisado por pares | En 410 estudiantes y 1024 encuentros, una sede mejoró puntajes OSCE y otra no; documenta efectos de institución y caso. | Soporte para una futura validación de utilidad | Evalúa el uso del simulador, no la procedencia desde una GPC ni la asignación estructural. |

## Síntesis: cómo se unen los puntos

La literatura no respalda una sola cadena ya establecida, pero sí sus componentes:

```text
GPC oficial
  │  Peleg / GLIF3 / Synthea / CPGPrompt
  ▼
representación estructurada y trazable
  │  Synthea / Takahashi / Bakkum / Sumpter / Liu
  ▼
casos candidatos
  │  Mayer / Fąferek / TIME / estándares de simulación
  ▼
blancos de cobertura educativa y compatibilidades
  │  CLRS / Hopcroft–Karp / test assembly
  ▼
asignación máxima y diagnóstico de déficits
```

Mayer et al. prueban que una colección necesita un *blueprint* antes de escribir los
casos. Fąferek et al. muestran empíricamente que un LLM puede omitir categorías,
añadir otras y producir redundancia aun cuando los casos individuales parezcan
aceptables después de revisión. La contribución del grafo es insertar una capa
determinista y auditable entre la generación y el uso: verificar qué objetivos tienen
casos compatibles, cuáles compiten por los mismos casos y cuáles no tienen ninguno.

Synthea aporta además una advertencia decisiva. Un modelo puede provenir de GPC y
mapas asistenciales y, aun así, producir distribuciones clínicamente inverosímiles.
Por tanto, la procedencia de una guía mejora trazabilidad, pero no prueba validez
clínica. De igual modo, un matching correcto prueba una propiedad combinatoria
condicionada a que los vértices y las aristas sean correctos; no valida esas aristas.

## Gap statement calibrado

> En la búsqueda dirigida de literatura primaria no se identificó un método que
> conecte, en una canalización reproducible, elementos trazables de una guía de
> práctica clínica, casos clínicos simulados y blancos educativos mediante un grafo
> bipartito, para después maximizar asignaciones uno-a-uno y localizar déficits de
> casos mediante emparejamiento máximo y la condición de Hall. Los antecedentes
> encontrados resuelven por separado la formalización de guías, la generación de
> pacientes o viñetas, el diseño de colecciones y la selección combinatoria de ítems.
> Este trabajo se plantea, por ello, como una prueba de concepto de integración
> metodológica y no como demostración de prioridad mundial ni como validación clínica.

Son apropiadas expresiones como “aplicación aparentemente no documentada dentro del
alcance revisado” o “integración metodológica novedosa”. Deben evitarse “primer método
mundial” y “casos clínicamente validados” mientras no exista una revisión sistemática
y una validación clínica independiente.

## Aporte preciso del proyecto

El resultado del emparejamiento no es “número de objetivos aprendidos”. Es:

> **Cobertura asignable:** máximo número de blancos educativos que puede recibir un
> caso compatible diferente bajo capacidades unitarias.

En símbolos, para el grafo bipartito $B=(U,V,E)$:

- $U$: casos clínicos simulados candidatos;
- $V$: blancos de cobertura educativa derivados de la GPC;
- $(u,v) \in E$: un panel acepta que el caso $u$ puede ser el vehículo principal
  para enseñar o evaluar el blanco $v$;
- $M$: asignación uno-a-uno sin repetir casos ni objetivos.

La pregunta matemáticamente exacta es:

> ¿Cuál es el máximo número de blancos educativos derivados de una GPC que puede
> asignarse uno a uno a casos clínicos simulados compatibles, si cada caso se utiliza
> una sola vez y cada blanco requiere un caso diferente?

Conviene usar “blanco de cobertura educativa” durante la extracción. Un elemento de
la GPC solo debe llamarse “objetivo de aprendizaje” después de que un docente lo
reformule con verbo observable, contenido, contexto y criterio, por ejemplo:
“identificar el criterio de severidad X en una paciente simulada”.

## Condición de aplicabilidad y modelos alternativos

El matching máximo es correcto solo si el diseño adopta deliberadamente esta regla:

> Cada caso se asigna como vehículo principal de exactamente un blanco durante una
> actividad, y cada blanco requiere un caso distinto.

Un caso real puede contener varios aprendizajes. Si se permite acreditar varios
objetivos con una sola utilización del caso, el matching uno-a-uno subestima la
cobertura. En esa extensión corresponderían:

- *maximum coverage* o *set cover*, si un caso acredita varios blancos;
- $b$-matching, si casos u objetivos tienen capacidades mayores que uno;
- matching ponderado, si importa calidad, prioridad o fidelidad clínica;
- programación lineal entera, si se agregan cuotas de dificultad, diversidad,
  tiempo, especialidad o nivel de evidencia.

Para la versión KISS del curso, el matching no ponderado conserva una pregunta clara,
un algoritmo clásico y una interpretación visual. La restricción uno-a-uno debe
aparecer en la pregunta, los métodos y las limitaciones.

## Validación científicamente proporcionada

La evidencia revisada sugiere separar al menos cuatro capas:

1. **Validez algorítmica.** Pruebas unitarias, comparación con otro solucionador,
   grafos exhaustivos pequeños y análisis de complejidad basado principalmente en
   CLRS; Hopcroft–Karp se cita como fuente histórica.
2. **Validez de contenido.** Especialistas clínicos y un educador revisan de forma
   independiente blancos, casos y aristas. El índice de validez de contenido puede
   seguir a Lynn y Polit, Beck y Owen; debe reportarse también el proceso de
   adjudicación y no solo un promedio.
3. **Validez estructural.** Cardinalidad máxima, blancos no asignados, vértices
   aislados y testigos de Hall. Esta capa mide cobertura asignable, no exactitud ni
   beneficio clínico.
4. **Validez educativa.** Revisión de claridad, realismo, utilidad y dificultad; un
   piloto con estudiantes puede ser exploratorio. La evaluación psicométrica y de
   resultados de aprendizaje requiere una muestra y un diseño posteriores.

La validación clínica y educativa no debe ser reemplazada por un LLM evaluador. Los
trabajos de Takahashi, Fąferek, Gierl y Huwendiek respaldan revisión humana,
instrumentos explícitos y reporte de variabilidad entre casos.

## Limitaciones de esta revisión y del posicionamiento

- La búsqueda fue dirigida y no registrada bajo PRISMA; puede haber trabajos no
  indexados o publicados en otros idiomas.
- Parte de la evidencia más cercana es preprint y debe presentarse con menor peso que
  la evidencia revisada por pares.
- Los trabajos sobre test assembly respaldan la transferencia matemática, pero no
  demuestran por sí mismos utilidad en educación médica.
- Las GPC son documentos normativos para atención; transformarlas en blancos
  educativos exige decisiones pedagógicas adicionales.
- La validez de las conclusiones estructurales depende de la exactitud de la
  extracción y de cada arista de compatibilidad.
- Un estudio con una sola GPC demuestra factibilidad y reproducibilidad interna, no
  generalización a otras guías, poblaciones o instituciones.
- El proyecto no debe utilizarse para diagnóstico, recomendación, priorización ni
  asignación de pacientes reales.

Las referencias bibliográficas estructuradas se encuentran en
[`references.bib`](references.bib).
