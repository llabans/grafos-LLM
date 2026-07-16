# Revisión de literatura: de una GPC a estructuras previas a datos sintéticos

## Pregunta de la revisión

¿Existe soporte científico para insertar una capa de matching bipartito entre
las variantes clínicas de ruta derivadas de una GPC y un catálogo finito de
estructuras de caso que servirán
como especificaciones de una generación sintética posterior?

La pregunta se descompuso en cuatro líneas:

1. representación computable de guías;
2. ejecución de rutas clínicas;
3. generación y evaluación de pacientes o registros sintéticos;
4. asignación combinatoria uno-a-uno.

La teoría algorítmica principal es CLRS, cuarta edición, capítulo 25. La
literatura biomédica justifica los objetos y sus controles, no modifica la
definición matemática del matching.

## Método

**Fecha de cierre:** 16 de julio de 2026, America/Lima.

Se realizó una búsqueda dirigida en PubMed, Crossref, OpenAlex, arXiv, medRxiv y
sitios editoriales. Se combinaron términos como:

- clinical practice guideline, computer-interpretable guideline, GLIF;
- guideline knowledge model, executable guideline, decision tree;
- synthetic patient, synthetic EHR, clinical trajectory;
- clinical consistency, fidelity, utility, privacy;
- bipartite matching, maximum matching, Hopcroft-Karp, Hall.

Se priorizaron artículos originales y preprints cercanos. La búsqueda no fue una
revisión sistemática registrada; por ello, el gap se formula como inferencia
calibrada y no como prueba de prioridad mundial.

## Evidencia primaria

| Fuente | Hallazgo útil | Relación con el proyecto | Límite |
|---|---|---|---|
| Peleg et al. (2003), [comparación de modelos de GPC computables](https://doi.org/10.1197/jamia.M1135) | Compara seis formalismos mediante fragmentos de GPC y explicita planes, decisiones, acciones y escenarios. | Sustenta transformar texto normativo en componentes ejecutables y trazables. | No aborda generación sintética ni selección combinatoria. |
| Boxwala et al. (2004), [GLIF3](https://doi.org/10.1016/j.jbi.2004.04.002) | Distingue niveles conceptual, computable e implementable; formaliza pasos de decisión y acción. | Sustenta el grafo dirigido y la necesidad de consistencia antes de ejecutar. | Orientado a soporte de decisión, no a manifiestos de generación. |
| Walonoski et al. (2018), [Synthea](https://doi.org/10.1093/jamia/ocx079) | Genera pacientes y EHR sintéticos mediante módulos, máquinas de estados y conocimiento clínico público, incluidas GPC. | Demuestra la cadena conocimiento clínico → estados → pacientes sintéticos. | Sus propias evaluaciones muestran que estructura y procedencia no bastan para garantizar realismo clínico o epidemiológico. |
| Zhang et al. (2020), [simulación de EMR](https://doi.org/10.1093/jamia/ocz161) | Propone un pipeline GAN y evalúa propiedades estructurales, utilidad predictiva y privacidad. | Sustenta separar generación de evaluación y medir varias dimensiones. | Aprende de EMR reales; no crea rutas desde una GPC ni usa matching. |
| Deng et al. (2026), [CPGPrompt](https://arxiv.org/abs/2601.03475) | Preprint que traduce GPC a árboles de decisión ejecutables y los prueba con viñetas sintéticas. Reporta mejor desempeño binario que multiclase y señala dificultades con negación y temporalidad. | Es el antecedente más cercano para GPC → árbol → ejecución de casos. Justifica resolver restricciones antes de redactar. | No crea un portafolio de estructuras ni optimiza asignaciones uno-a-uno. |
| Zhou et al. (2026), [consistencia de trayectorias sintéticas](https://arxiv.org/abs/2603.06720) | Preprint que separa fidelidad estadística, consistencia clínica, utilidad y privacidad. En una revisión pequeña, alta concordancia estadística coexistió con inconsistencias clínicas. | Refuerza la separación de validez estructural, clínica y generativa. | Usa MIMIC-IV y auditoría posterior; no deriva rutas de una GPC. |
| Hopcroft y Karp (1973), [algoritmo original](https://doi.org/10.1137/0202019) | Introduce el algoritmo para matching máximo bipartito. | Antecedente histórico de la solución y su cota. | La exposición del curso sigue prioritariamente a CLRS. |
| Hall (1935), [sistemas de representantes](https://doi.org/10.1112/jlms/s1-10.37.26) | Caracteriza la existencia de representantes distintos. | Permite explicar por qué ocho rutas con siete estructuras vecinas no tienen asignación perfecta. | No valida la semántica clínica de vértices o aristas. |

## Cómo se unen los puntos

La cadena apoyada por la literatura puede expresarse así:

    GPC narrativa
      │  Peleg / GLIF3
      ▼
    modelo computable y grafo de decisión
      │  CPGPrompt
      ▼
    variantes ejecutables y casos de prueba
      │  propuesta de este proyecto
      ▼
    estructuras de caso + compatibilidad demostrable
      │  CLRS / Hopcroft-Karp / Hall
      ▼
    assignment_manifest.json óptimo uno-a-uno
      │  Synthea / Zhang / Zhou
      ▼
    generación y evaluación sintética posterior

Peleg y GLIF3 justifican el paso de texto a lógica explícita. Synthea demuestra
que máquinas de estados basadas en conocimiento clínico pueden alimentar una
generación completa. CPGPrompt muestra que las GPC pueden convertirse en
árboles navegables, pero también que negación, temporalidad y decisiones
multiclase siguen siendo puntos frágiles. Zhang y Zhou muestran que una salida
sintética debe evaluarse por más de una dimensión.

El matching se ubica antes de esos generadores. No busca mejorar directamente
un GAN o un LLM; garantiza que el plan inicial reserve estructuras distintas
para tantas rutas como sea posible y declara la capacidad faltante.

## Gap statement

> Dentro de la búsqueda dirigida no se identificó una publicación que conecte
> en una sola canalización reproducible: una GPC congelada, un grafo dirigido,
> variantes clínicas de ruta completas, estructuras de caso todavía no instanciadas,
> compatibilidad demostrada por ejecución, matching máximo uno-a-uno y un
> manifiesto previo a generación sintética.

Esta conclusión es una **inferencia a partir del conjunto revisado**. Son
apropiadas las expresiones “integración aparentemente no documentada en la
búsqueda” y “prueba de concepto potencialmente novedosa”. No es defendible
afirmar “primer método mundial”.

## Aporte preciso

La contribución es una capa de **capacidad estructural pre-generativa** para un
catálogo piloto con capacidad unitaria:

\[
\theta(B)=|M^*|.
\]

\(\theta(B)\) es el máximo número de rutas que pueden reservar una estructura
independiente bajo capacidades unitarias. No es:

- cobertura clínica poblacional;
- prevalencia de rutas;
- realismo sintético;
- exactitud diagnóstica;
- utilidad para un modelo downstream.

## Por qué la estructura previa es relevante

Una generación narrativa puede parecer plausible y, aun así:

- violar una condición de entrada;
- omitir una negación;
- mezclar ramas incompatibles;
- alcanzar un terminal equivocado;
- repetir excesivamente una misma trayectoria;
- mantener distribuciones marginales pero romper relaciones clínicas.

La arista existencial con testigo reduce los primeros cuatro riesgos antes de
generar. No resuelve los dos últimos, que requieren evaluación generativa.

## Condición de aplicabilidad

Matching máximo es correcto si cada ruta debe recibir una estructura
independiente y cada estructura se reserva una sola vez en el manifiesto KISS.
Si una estructura puede contarse simultáneamente para varias rutas, el problema
cambia:

- set cover: mínimo conjunto reutilizable que alcanza todas las rutas;
- maximum coverage: máxima cobertura con presupuesto fijo;
- \(b\)-matching: capacidades mayores que uno;
- matching ponderado: prioridad o fidelidad desigual;
- programación entera: cuotas, prevalencias, diversidad o tamaños de muestra.

## Implicaciones para validación

La literatura obliga a mantener cuatro capas:

1. **Algorítmica:** optimalidad y complejidad según CLRS.
2. **Estructural:** rutas alcanzables, testigos, aristas y Hall.
3. **Clínica:** fidelidad de predicados y acciones a la GPC por revisión
   independiente.
4. **Generativa:** fidelidad estadística, consistencia clínica, diversidad,
   utilidad y privacidad de datos ya producidos.

La concordancia entre solvers solo informa la primera. La revisión clínica no
sustituye pruebas de privacidad o utilidad downstream.

## Limitaciones de la revisión

- búsqueda dirigida, no PRISMA;
- posible omisión de literatura no indexada o en otros idiomas;
- dos antecedentes cercanos son preprints;
- una sola GPC en la prueba de concepto;
- transferencia conceptual desde sistemas generativos con fuentes distintas;
- ausencia de evaluación empírica de datos sintéticos, porque todavía no se
  generan en este proyecto.

Las referencias estructuradas se encuentran en [references.bib](references.bib).
