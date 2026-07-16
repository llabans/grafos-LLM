# Auditoría semántica del grafo dirigido

## Propósito

Determinar qué subgrafo puede ejecutarse de forma parcial y determinista antes
de construir variantes de ruta. El matching no corrige ambigüedades del grafo
clínico.

## flow_1

- seis nodos y cinco aristas;
- sin ciclos;
- dos salidas positivas simultáneas documentadas como semántica AND;
- útil para el pipeline completo, pero excluido de la demo KISS XOR.

Tratar esas salidas como alternativas eliminaría una acción sustentada.

## flow_2

- nueve nodos y siete aristas;
- inicio reconciliado;
- decisiones Sí/No y Con criterios/Sin criterios como XOR;
- un nodo informativo aislado que no es terminal alcanzable;
- sin ciclos en el subgrafo clínico.

La demo KISS se limita a este subgrafo. En un nodo XOR, una asignación válida
habilita exactamente un sucesor. Una asignación incompleta o contradictoria
hace que \(\operatorname{Exec}_D\) no esté definida y produce rechazo.

## flow_3

Describe el método de evidencia de la guía, no una trayectoria clínica. Se
conserva en la auditoría documental y se excluye de \(D\), \(U\), \(V\) y \(E\)
para este proyecto.

## Invariantes

- un solo inicio válido;
- terminales alcanzables;
- endpoints existentes;
- etiquetas XOR exclusivas;
- no se atraviesa el nodo aislado;
- cada variante conserva la secuencia completa;
- la canonical_signature ignora IDs accidentales;
- el witness_assignment reproduce el terminal declarado.

## Resultado

El subgrafo XOR de flow_2 es suficiente para la instancia KISS. La fuente local
privada es necesaria para reconstruir textos, páginas y predicados exactos.
