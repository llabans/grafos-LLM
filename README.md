# Estructuras de caso clínico antes de generar datos sintéticos

Versión KISS del proyecto final de Algoritmos. El repositorio implementa una
capa combinatoria intermedia entre una guía de práctica clínica estructurada y
la futura generación de datos clínicos sintéticos.

La unidad de trabajo no es todavía un paciente ni una historia redactada. Es una
**estructura de caso clínico**: un objeto parametrizable con variables, dominios,
restricciones lógicas, estado inicial, missingness permitido y procedencia.

## Pregunta del proyecto

> ¿Cómo asignar un catálogo finito de estructuras de caso clínico a variantes
> clínicas de ruta derivadas de una GPC para maximizar el número de
> asignaciones válidas uno-a-uno antes de generar los casos sintéticos?

Versión breve:

> ¿Cuántas rutas diferentes de una guía pueden recibir estructuras diferentes,
> sin usar una misma estructura dos veces?

## Lugar exacto en el proceso

    GPC oficial congelada
        ↓
    grafo dirigido de decisión
        ↓
    variantes clínicas de ruta completas y trazables
        ↓
    estructuras de caso clínico sin narrativa
        ↓
    compatibilidad lógica estructura-ruta
        ↓
    matching máximo bipartito
        ↓
    assignment_manifest.json
        ↓
    instancias clínicas y datos sintéticos futuros

El proyecto termina en **assignment_manifest.json**. La asignación de valores,
la redacción narrativa y la producción masiva de registros quedan fuera del
alcance actual.

## Modelo bipartito

Sea \(B=(U,V,E)\):

- \(U\): catálogo finito de estructuras de caso clínico para un lote piloto,
  cada entrada con capacidad unitaria;
- \(V\): variantes clínicas de ruta por representar, tipo
  **ClinicalRouteVariant**;
- \((u,v)\in E\): existe al menos una instancia permitida por \(u\) cuya
  ejecución sobre el grafo de decisión recorre exactamente \(v\);
- \(M\): asignaciones uno-a-uno estructura-ruta.

Formalmente:

\[
(u,v)\in E
\iff
\exists x\in \operatorname{Inst}(u):
\operatorname{Exec}_D(x)=v.
\]

Las variantes se deduplican mediante **canonical_signature**, que ignora el ID.
La función \(\operatorname{Exec}_D\) es parcial y determinista sobre el subgrafo
XOR: una instancia válida habilita exactamente una rama; datos insuficientes o
contradictorios producen rechazo. Cada arista persiste el
**witness_assignment** que la demuestra.

El objetivo es \(\max |M|\), con cada entrada del catálogo y cada variante
utilizadas a lo sumo una vez.

## Instancia KISS preespecificada

La demostración pública utiliza identificadores simbólicos y conserva solo la
estructura mínima necesaria:

| Componente | Conteo |
|---|---:|
| estructuras de caso \(U\) | 7 |
| variantes clínicas de ruta \(V\) | 8 |
| aristas de compatibilidad \(E\) | 14 |
| matching máximo \(M^*\) | 7 |

Las ocho variantes son siete trayectorias con un criterio de severidad focal y una
trayectoria completa sin severidad. Cada estructura declara los siete criterios:
permite activar su criterio focal manteniendo controlados los demás, y también
permite fijar los siete como ausentes. Por eso cada estructura tiene dos aristas:
una hacia su ruta severa focal y otra hacia la ruta común sin severidad.

La reconstrucción exacta de textos, nodos y páginas requiere el snapshot local
privado y congelado de la GPC. La demo pública no expone ese material.

## Resultado y certificado

\[
|M^*|=7.
\]

La igualdad se certifica por dos cotas:

1. se construye un matching factible de siete pares, luego
   \(|M^*|\geq 7\);
2. solo existen siete estructuras, luego \(|M^*|\leq 7\).

Además, para el conjunto \(S\) de las ocho variantes,
\(|S|=8>|N(S)|=7\). La condición de Hall muestra un déficit estructural de una
variante bajo la política uno-a-uno. El algoritmo no decide qué variante tiene mayor
importancia clínica; para ello se necesitarían pesos o restricciones adicionales.

## Base teórica

La fuente principal es Cormen, Leiserson, Rivest y Stein, *Introduction to
Algorithms*, cuarta edición, capítulo 25. El proyecto utiliza:

- definición de matching y matching máximo;
- caminos alternantes y aumentantes;
- diferencia simétrica \(M\oplus P\);
- criterio de optimalidad por ausencia de caminos aumentantes;
- Hopcroft-Karp y su procesamiento por capas;
- condición de Hall como explicación de la imposibilidad de matching perfecto.

Se implementan un baseline por caminos aumentantes y Hopcroft-Karp. La cota
asintótica de Hopcroft-Karp es \(O(|E|\sqrt{|V_B|})\), donde \(V_B=U\cup V\).
Para \(n=|U|+|V|\), \(m=|E|\) y costo de compatibilidad
\(C_{\mathrm{compat}}\), la cota de ingeniería completa es:

\[
T_{\mathrm{routes}}+T_{\mathrm{structures}}+
O(|U||V|C_{\mathrm{compat}})+O(n+m\sqrt n).
\]

## Hipótesis de trabajo

> Si las variantes se derivan del grafo congelado, las estructuras se
> construyen por una vía independiente desde el esquema permitido y las aristas
> se aprueban mediante ejecución lógica reproducible, entonces el matching máximo
> produce un manifiesto uno-a-uno de cardinalidad óptima y revela variantes que no
> pueden recibir una estructura independiente.

La hipótesis es algorítmico-estructural. No afirma realismo clínico ni utilidad
de los datos sintéticos aún no generados.

## Capas de validez

- **Algorítmica:** correctitud del solver, pruebas y concordancia entre métodos.
- **Estructural:** exactitud de particiones, aristas, cardinalidad y testigos de
  déficit.
- **Clínica:** fidelidad de variantes, restricciones y witness_assignments a
  la GPC, evaluada por especialistas independientes.
- **Generativa:** coherencia clínica, fidelidad de variante, diversidad, privacidad
  y utilidad de las instancias sintéticas; corresponde a una fase posterior.

Una capa no sustituye a otra. Un matching correcto sobre aristas equivocadas
sigue siendo clínicamente inválido.

## Productos

- [Informe KISS](docs/kiss_project_report.md)
- [Formulación matemática](docs/problem_formulation.md)
- [Metodología](docs/methodology.md)
- [Revisión de literatura](docs/literature_review.md)
- [Validación académica y científica](docs/kiss_academic_validation.md)
- [Protocolo de validación](docs/validation_protocol.md)
- [Explicación para medicina y epidemiología](docs/kiss_student_explanation.md)
- [Mapeo a CLRS, capítulo 25](docs/chapter_25_project_mapping.md)
- [Guion de exposición](docs/presentation_outline.md)
- [Cumplimiento de la rúbrica](docs/rubric_compliance.md)

## Correspondencia con la rúbrica

| Requisito | Evidencia |
|---|---|
| teoría | capítulo 25, formulación y demostración de optimalidad |
| análisis | complejidad, Hall, hipótesis y límites |
| aplicación | capa previa a generación clínica sintética desde una GPC |
| código | implementaciones propias, pruebas y oráculo independiente |
| Colab | notebook reproducible del caso KISS |
| material adicional | documentación, protocolo y ficha de una página |
| exposición | narrativa de 15 minutos con GOAL y LOOP |

## Alcance responsable

Este software no diagnostica, prescribe, prioriza pacientes ni valida una GPC.
Tampoco genera todavía historias clínicas completas. Su resultado es un plan
combinatorio trazable, **assignment_manifest.json**, para una futura etapa de
generación sintética.
