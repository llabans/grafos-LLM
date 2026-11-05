# Limitaciones y amenazas a la validez

## 1. Validez de constructo

La cardinalidad \(|M^*|\) mide capacidad de asignación uno-a-uno. No mide
realismo, frecuencia de rutas, calidad clínica, utilidad ni privacidad.

## 2. Dependencia de las aristas

El solver puede ser perfecto y el resultado inútil si una compatibilidad es
incorrecta. Cada arista necesita testigo reproducible y revisión clínica.

## 3. Restricción unitaria

Reservar una estructura para una sola ruta es una política KISS. Una estructura
parametrizable podría generar varias rutas en una canalización real. La
restricción hace visible la capacidad independiente, pero puede subestimar la
capacidad reutilizable.

## 4. Matching no ponderado

Todos los pares cuentan igual. El algoritmo no expresa prioridad, riesgo,
prevalencia, costo ni calidad. Si esas diferencias importan, se requieren pesos
o restricciones.

## 5. Una sola GPC

La factibilidad interna no demuestra transportabilidad a otras guías,
especialidades, instituciones o versiones.

## 6. Fuente privada

La demo pública usa IDs simbólicos. Sin el snapshot congelado no puede auditarse
externamente cada texto y página, aunque la topología algorítmica sí sea
reproducible.

## 7. Rutas canónicas

La enumeración de variantes depende de decisiones sobre ciclos, equivalencias y
terminales. Otra **canonical_signature** válida puede producir otro \(V\).

## 8. Expresividad de las estructuras

Una estructura demasiado rígida pierde variantes; una demasiado flexible se vuelve
compatible con casi todo y reduce el valor informativo del grafo. La
granularidad debe justificarse.

## 9. Existencia no equivale a robustez

Una arista se acepta con al menos un testigo. Eso no indica qué proporción del
dominio de la estructura recorre la ruta ni cuán estable es ante perturbaciones.
Una extensión puede estimar robustez o volumen factible.

## 10. Hall no asigna causa clínica

El déficit identifica un cuello combinatorio. Determinar si debe añadirse una
estructura, eliminarse una variante o cambiarse la política es una decisión externa.

## 11. No hay datos sintéticos todavía

No pueden evaluarse fidelidad estadística, diversidad, utilidad downstream ni
privacidad. Cualquier afirmación sobre esas dimensiones sería prematura.

## 12. Evidencia bibliográfica

La búsqueda fue dirigida y no registrada como revisión sistemática. El gap es
una inferencia calibrada, no una prueba de originalidad mundial.

## 13. Validez clínica pendiente

La procedencia desde una GPC no garantiza que su extracción sea correcta ni que
la guía sea aplicable fuera de su población y contexto. Se requiere panel
independiente.

## 14. Riesgo de automatización

Un LLM puede ayudar a realizar texto futuro, pero no debe crear variables,
alterar rutas o aprobar su propia salida sin controles externos.

## 15. Cambios de versión

Una nueva GPC puede modificar variantes y aristas. Los resultados son válidos solo
para los hashes declarados y deben invalidarse ante drift.

## Mitigaciones

- versionado y hashes;
- testigos positivos y negativos;
- tres solvers;
- panel clínico independiente;
- reporte de todos los aislados y déficits;
- lenguaje de inferencia limitado;
- validación generativa separada;
- réplica futura con otra GPC.
