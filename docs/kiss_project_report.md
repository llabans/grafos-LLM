# Informe principal — versión KISS

## Título

**Emparejamiento bipartito para asignar casos clínico-educativos derivados de
una GPC a objetivos de aprendizaje distintos**

## Resumen

Se propone una capa de curación combinatoria para bancos de casos educativos
derivados de guías de práctica clínica. La pregunta no es cómo diagnosticar o
tratar pacientes, sino cómo asignar casos candidatos a objetivos educativos sin
reutilizar un caso ni contar dos veces un objetivo. El problema se formaliza como
matching máximo en un grafo bipartito.

La demostración usa una vista preespecificada de la GPC
`gpc-05-hipertension-embarazo-2025`: siete escenarios simbólicos asociados a
siete criterios explícitos de severidad y ocho microobjetivos —los siete
criterios y una ruta/BPC común de severidad—. Cada escenario se conecta con su
criterio y con la BPC; el grafo contiene 7 vértices a la izquierda, 8 a la derecha
y 14 aristas. Dos implementaciones propias obtienen matching máximo de
cardinalidad 7. El testigo de Hall `8>7` prueba que la cobertura perfecta es
imposible bajo unicidad.

La literatura respalda por separado la representación computable de guías, el
uso de grafos para preservar sus relaciones y la utilidad de simulaciones en
educación médica. La revisión no identificó, dentro del protocolo documentado,
una integración exacta de GPC estructurada, casos trazables, objetivos
educativos, matching máximo y certificado de Hall. El proyecto se posiciona por
ello como una combinación potencialmente novedosa y científicamente
fundamentada, pero no como una intervención clínica o educativa ya validada.

## 1. Problema y relevancia

La generación de casos desde una guía puede producir muchos candidatos, pero no
garantiza que el banco final sea diverso ni que cada objetivo tenga un
representante distinto. La inspección manual tampoco demuestra que la selección
sea máxima. El problema intermedio es de **curación y cobertura**:

1. una guía estructurada aporta criterios y rutas;
2. reglas explícitas generan o identifican casos candidatos;
3. una regla de compatibilidad vincula casos con microobjetivos;
4. un matching selecciona el mayor número de representantes uno-a-uno;
5. un testigo de Hall explica cualquier brecha.

El matching no redacta por sí mismo una viñeta clínica completa. Se ubica entre
la generación de candidatos y la validación experta: organiza, selecciona y hace
auditable la cobertura.

## 2. Pregunta y objetivo

### Pregunta

> ¿Cómo asignar, uno a uno, escenarios clínico-educativos simulados compatibles
> a microobjetivos de aprendizaje sobre severidad para maximizar el número de
> microobjetivos cubiertos, sin reutilizar casos?

### GOAL

Maximizar microobjetivos distintos representados por casos distintos, con
compatibilidad trazable y cero decisiones clínicas.

### Estimando computacional

Para un grafo bipartito fijado `B=(U,V,E)`, se estima de forma determinista:

\[
\theta(B)=\max_{M\subseteq E}\{|M|:M\text{ es matching}\}.
\]

No es un parámetro poblacional. No requiere intervalo de confianza porque no se
obtiene de una muestra aleatoria.

## 3. Material

Se utiliza una sola fuente:

```text
gpc-05-hipertension-embarazo-2025
```

La aplicación KISS se limita al subgrafo de severidad del segundo flujograma.
Los siete casos son escenarios simbólicos, uno por criterio explícito. Los ocho
microobjetivos fueron operacionalizados para el proyecto; no son objetivos
curriculares oficiales de MINSA.

## 4. Modelo bipartito

- `U`: siete escenarios clínico-educativos simbólicos `C1,...,C7`.
- `V`: siete objetivos de identificación de criterio más un objetivo de
  reconocimiento de la ruta/BPC asociada.
- `E`: compatibilidades estructurales aprobadas.

Cada caso tiene exactamente dos aristas:

\[
E=\{(C_i,O_i):1\leq i\leq7\}\cup
  \{(C_i,O_{BPC}):1\leq i\leq7\}.
\]

Así, `|U|=7`, `|V|=8` y `|E|=14`.

## 5. Algoritmo

La columna vertebral es el capítulo 25 de CLRS. Se implementaron:

- un baseline por caminos aumentantes;
- Hopcroft-Karp, con BFS por capas y DFS restringido;
- extracción de testigos de déficit de Hall.

El criterio de Berge establece que un matching es máximo si y solo si no existe
un camino aumentante. Hopcroft-Karp procesa varios caminos aumentantes mínimos
por fase y tiene cota clásica `O(E√V)`, según el artículo original de
[Hopcroft y Karp (1973)](https://epubs.siam.org/doi/10.1137/0202019) y el
tratamiento de CLRS.

## 6. Resultado

```text
PASS |U|=7 |V|=8 |E|=14 |M*|=7
agreement dfs=7 hopcroft_karp=7
hall_witness |S|=8 |N(S)|=7 deficiency=1
```

La optimalidad puede comprobarse sin confiar ciegamente en el software:

1. el solver construye siete pares, luego `|M*|≥7`;
2. ningún matching puede usar más de siete casos, luego `|M*|≤7`;
3. para los ocho objetivos, el vecindario tiene siete casos, es decir,
   `|S|=8>|N(S)|=7`.

Por tanto, `|M*|=7`.

## 7. Interpretación educativa

El grafo convierte una intuición en una decisión verificable: bajo la política
“un representante distinto por objetivo”, el banco actual no puede representar
los ocho microobjetivos. Existen dos respuestas de diseño:

1. añadir un octavo caso compatible e independiente;
2. permitir que un caso acredite varios objetivos y cambiar el modelo.

La segunda opción no es incorrecta; corresponde a una pregunta distinta, como
máxima cobertura, *set cover* o `b`-matching.

El matching no ponderado tampoco decide cuál objetivo debe quedar sin
representante. Si existen prioridades pedagógicas o clínicas, deben declararse
como pesos o restricciones antes de resolver.

## 8. Relación con la literatura

La propuesta une tres líneas que suelen aparecer separadas:

1. **Guías computables y grafos.** Los modelos GLIF y los trabajos recientes de
   grafos de decisión muestran que una GPC puede transformarse en una
   representación computable preservando relaciones y contexto. Un ejemplo
   reciente usa grafos de decisión para consultas sobre GPC
   ([Kandula y Bhattacharyya, 2023](https://arxiv.org/abs/2308.02984)); otro
   automatiza modelos gráficos de guías oncológicas y evalúa clasificación de
   nodos y relaciones
   ([Gupta et al., 2025](https://arxiv.org/abs/2501.13984)).
2. **Simulación clínica educativa.** Sistemas como
   [MedSimAI](https://arxiv.org/abs/2503.05793) muestran que las simulaciones
   escalables pueden integrarse con objetivos y evaluación formativa; otros
   trabajos usan fuentes curadas o representaciones controlables para reducir
   contenido no sustentado.
3. **Asignación combinatoria.** CLRS, Berge y Hopcroft-Karp proporcionan una
   teoría madura para construir y certificar asignaciones máximas uno-a-uno.

La contribución local no es afirmar que los grafos “validan la medicina”. Es
insertar una capa de cobertura óptima y explicable entre la estructuración de la
guía y el banco de casos.

## 9. Validez

### Ya demostrado

- correctitud estructural del grafo `7-8-14`;
- matching factible y máximo de cardinalidad 7;
- concordancia de dos implementaciones propias;
- testigo de Hall con déficit uno;
- reproducibilidad sin datos privados;
- trazabilidad al pipeline técnico completo.

### Aún no demostrado

- realismo y seguridad de viñetas clínicas completas;
- validez de contenido de los microobjetivos por panel independiente;
- efecto sobre aprendizaje, desempeño o retención;
- utilidad del flujo para docentes en comparación con selección manual;
- generalización a otra GPC.

Estas brechas no se ocultan. Se convierten en el protocolo de la siguiente fase.

## 10. LOOP de investigación

```text
DEFINIR → CONSTRUIR → RESOLVER → VERIFICAR → VALIDAR → INTERPRETAR → REPETIR
```

El LOOP distingue verificación algorítmica de validación de contenido. Un gate
verde en código no reemplaza el juicio experto.

## 11. Conclusión

La respuesta KISS es simple: siete casos distintos cubren como máximo siete de
ocho microobjetivos cuando cada caso se usa una vez. La relevancia científica
está en cómo se llega a esa respuesta: fuente estructurada, compatibilidad
trazable, algoritmo con garantía, certificado de brecha y límites explícitos.

El proyecto no genera evidencia clínica. Propone una herramienta reproducible
para diseñar y auditar bancos de casos derivados de guías, y deja preparado un
protocolo empírico para validar contenido y utilidad educativa.
