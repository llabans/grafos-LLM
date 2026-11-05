# Explicación KISS para tu perfil

## La idea médica

Una GPC contiene decisiones y rutas. Antes de pedirle a un generador que invente
pacientes, necesitamos comprobar que nuestras estructuras permiten representar
esas rutas sin contradicción.

## La idea epidemiológica

Es como revisar una ficha antes de recolectar datos. Si la ficha no puede
representar un estrato, ninguna cantidad de observaciones reparará ese defecto.

## La idea algorítmica

Construimos dos grupos:

- \(U\): siete entradas de un catálogo de estructuras;
- \(V\): ocho variantes clínicas de ruta.

Una arista significa:

> Existe al menos una asignación de valores permitida por la estructura que,
> ejecutada en el grafo de la GPC, recorre exactamente esa variante.

Cada arista guarda esa asignación como witness_assignment.

## Por qué “estructura de caso”

Todavía no hay nombre, edad concreta, historia ni prosa. Solo existen variables,
dominios, restricciones y fuente.

    estructura → instancia → registro sintético
        aquí         después          después

## La demo

Las ocho variantes son:

- siete con un criterio de severidad focal;
- una sin severidad.

Cada estructura \(S_i\) contiene los siete criterios y puede instanciar:

- su variante focal \(R_i\);
- la variante común \(R_0\) con todos ausentes.

Por eso hay catorce aristas.

## Qué optimizamos

No optimizamos el número de estructuras seleccionadas: serían siete y eso sería
trivial. Optimizamos el número de pares distintos:

\[
\max |M|.
\]

Cada estructura y variante aparecen como máximo una vez.

## Resultado

\[
|U|=7,\quad|V|=8,\quad|E|=14,\quad|M^*|=7.
\]

Hay una solución con siete pares y no puede haber ocho porque solo existen siete
entradas en el catálogo.

Hall lo expresa como:

\[
8\text{ variantes}>7\text{ estructuras vecinas}.
\]

## Qué aporta

Detecta la insuficiencia antes de generar datos. Permite:

- agregar una estructura;
- aceptar una variante libre;
- declarar prioridades;
- cambiar a un modelo que permita reutilización.

## Qué no aporta todavía

- pacientes sintéticos;
- realismo clínico;
- distribuciones epidemiológicas;
- privacidad;
- utilidad para modelos predictivos.

Esas propiedades se evalúan después.

## Producto final

**assignment_manifest.json** registra pares, testigos, hashes, variante libre y
estado de validación.

## Frase para exponer

> El grafo no genera pacientes: verifica si el plan estructural tiene capacidad
> para representar las rutas antes de comenzar la generación.
