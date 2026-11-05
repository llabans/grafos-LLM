# Arquitectura del pipeline

## Dos grafos, dos funciones

    GPC estructurada
          │
          ▼
    D = grafo dirigido de decisión
          │  enumera trayectorias completas
          ▼
    V = variantes clínicas de ruta por representar

    variables + dominios + restricciones
          │
          ▼
    U = estructuras de caso clínico

    U × V
      │  testigo de ejecución compatible
      ▼
    B = grafo bipartito
      │  matching máximo
      ▼
    assignment_manifest.json
      │
      ▼
    generación sintética posterior

El grafo dirigido \(D\) representa secuencia y decisión. El grafo bipartito
\(B\) representa posibilidad de asignación. Mezclarlos impediría interpretar
correctamente una arista.

## Capas

| Capa | Responsabilidad | Producto |
|---|---|---|
| fuente | congelar y reconciliar la GPC | manifiesto con hashes |
| semántica | construir \(D\), rutas y restricciones | objetos trazables |
| compatibilidad | ejecutar testigos | aristas justificadas |
| optimización | resolver \(B\) | matching, déficit y assignment_manifest.json |
| generación | instanciar y realizar datos | fuera del alcance actual |

## Invariantes

- ninguna variable clínica se agrega sin fuente;
- ninguna variante se acepta sin ser alcanzable ni canonical_signature única;
- ninguna arista se publica sin testigo;
- una entrada del catálogo y una variante aparecen a lo sumo una vez en el matching;
- una salida algorítmica no se etiqueta como validación clínica;
- la futura redacción no puede alterar la ruta asignada.
