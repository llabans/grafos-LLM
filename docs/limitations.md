# Limitaciones y amenazas a la validez

## Alcance clínico

El proyecto no valida el contenido médico de la GPC ni traduce sus elementos en recomendaciones para personas. No incorpora historias clínicas, pacientes sintéticos, resultados, dosis, pronósticos ni priorización. Una compatibilidad es una relación de cobertura educativa, no una indicación clínica.

## Dependencia de fuente

- Solo se autoriza `gpc-05-hipertension-embarazo-2025`.
- La variante resumida está excluida porque su mapeo es `draft`.
- Los archivos Phase 4 contienen múltiples guías; un error de filtro sería grave.
- Los hashes de Phase 4 cubren el archivo multiguía completo: un cambio ajeno a la guía objetivo puede disparar drift conservador.
- Los agregados no incluyen esquemas formales completos; algunos contratos son validaciones de runtime derivadas del snapshot inspeccionado.
- No se versiona el ZIP, por lo que la reproducción por terceros exige acceso autorizado independiente.

## Modelado semántico

- Las firmas son reglas locales versionadas porque `route_templates` está vacío.
- El `AND` de `flow_1` se apoya en una advertencia textual de la fuente; no debe generalizarse a otras guías.
- `flow_2:n9` se conserva como aislado y no como terminal alcanzable; otra finalidad documental podría tratarlo de modo distinto.
- `flow_3` se excluye por ser metodológico.
- La normalización convierte solo estructuras explícitas; puede omitir conceptos que requieran interpretación humana.

## Constructo de cobertura

“Cobertura” significa objetivo con representante único bajo la función de compatibilidad. La métrica no captura importancia relativa, dificultad, redundancia pedagógica ni posibilidad de que un escenario ilustre varios objetivos en la práctica. La restricción uno-a-uno crea competencia intencional; un modelo de *set cover* respondería otra pregunta.

No hay ponderación. Si los objetivos tuviesen prioridades justificadas, el problema sería asignación ponderada y exigiría otra formulación y evidencia.

## Correctitud algorítmica

La teoría sustenta el algoritmo y 689 grafos pequeños fueron verificados exhaustivamente, pero el software no está formalmente probado con un asistente de teoremas. Los tests no pueden demostrar ausencia absoluta de defectos. NetworkX reduce el riesgo de error correlacionado, sin eliminarlo.

La función de testigos de Hall presupone un matching máximo; se usa después de concordancia entre dos solvers y oráculo.

## Experimentos

- Los tiempos son microbenchmarks de un entorno y fecha concretos.
- Las 21 repeticiones comparten hardware, proceso e intérprete; no son observaciones independientes para inferencia estadística.
- `tracemalloc` estima asignaciones Python, no memoria residente total.
- El fixture escalera es adversarial para el DFS determinista y no representa una población de grafos.
- El grafo GPC es pequeño; diferencias de microsegundos no justifican una conclusión práctica fuerte.
- No se evaluó paralelización, otras implementaciones, lenguajes ni grandes colecciones de guías.

## Validez externa

Los resultados numéricos no se transfieren a otra GPC, versión, país, idioma o pipeline de extracción. Adaptar el método requiere volver a ejecutar INSPECT, definir contratos, reconciliar semántica, versionar reglas y repetir todos los gates.

## Riesgo de interpretación

Los términos médicos pueden hacer que el lector sobreinterprete el producto. Por ello todos los entregables reiteran:

- uso educativo y no clínico;
- ausencia de pacientes;
- ausencia de inferencia causal o predictiva;
- “sin arista” como falta de soporte estructural, no como juicio médico;
- 94,3 % como métrica combinatoria, no clínica.

## Trabajo futuro permitido

Dentro del mismo alcance educativo podrían estudiarse:

- sensibilidad de `|M|` a versiones alternativas, explícitas y revisadas de compatibilidad;
- matching ponderado con pesos no clínicos justificados, por ejemplo costo de construcción de una prueba;
- comparación con *set cover* como problema distinto;
- contratos JSON Schema oficiales;
- property-based testing adicional;
- prueba formal del solver;
- benchmarks en familias sintéticas con diseño factorial de tamaño y densidad.

Ninguna extensión debe convertir el proyecto en soporte de decisión clínica sin un proceso independiente de regulación, seguridad, evaluación clínica y gobernanza que está fuera de este curso.
