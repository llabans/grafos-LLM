# Mapa Capítulo 25 -> proyecto

| Concepto del capítulo | Página/sección verificada | Artefacto | Implementación prevista | Prueba prevista | Diapositiva | Estado |
|---|---|---|---|---|---:|---|
| Matching y máximo | imp. 704-705 / PDF 911-913; §25/25.1 | `problem_formulation.md` | `matching/graph.py` | invariantes | 2, 6 | Verificado |
| Maximal vs máximo | imp. 705 / PDF 913; §25.1 | `chapter_25_study_notes.md` | documentación | óptimo exhaustivo | 7 | Verificado |
| Camino alternante/aumentante | imp. 705-706 / PDF 913-914; §25.1 | `methodology.md` | `augmenting_path.py` | casos conocidos | 7 | Verificado |
| Diferencia simétrica | imp. 706 / PDF 914-915; Lema 25.1 | `methodology.md` | reasignación recursiva | cardinalidad +1 | 7 | Verificado |
| Caminos disjuntos | imp. 706-707 / PDF 915; Cor. 25.2 | `methodology.md` | fase HK | aumentos por fase | 8 | Verificado |
| Criterio de optimalidad | imp. 707-708 / PDF 916-917; Cor. 25.4 | `problem_formulation.md` | condición de parada | 689 grafos + oráculos | 7 | Verificado |
| Baseline DFS | imp. 708 / PDF 917; adaptación | `methodology.md` | `augmenting_path.py` | paridad DFS/HK | 8, 9 | Adaptación explícita |
| HOPCROFT-KARP | imp. 709 / PDF 918; §25.1 | `methodology.md` | `hopcroft_karp.py` | determinismo | 8 | Verificado |
| BFS por capas | imp. 710-711 / PDF 919-921; §25.1 | `methodology.md` | `build_layers` | fases BFS | 8 | Verificado |
| DFS restringido | imp. 712 / PDF 922; §25.1 | `methodology.md` | `augment_layered` | caminos admisibles | 8 | Verificado |
| Complejidad HK | imp. 713-715 / PDF 923-926; Teo. 25.8 | `academic_validation.md` | instrumentación | benchmark, sin inferencia clínica | 9 | Verificado |
| Déficit de Hall | imp. 715 / PDF 926-927; ejercicio | `academic_validation.md` | `matching/analysis.py` | testigos `8>7` y `1>0` | 9 | Extensión demostrada |
| Método húngaro | imp. 723-739 / PDF 936-958; §25.3 | comparación | no implementado | no aplica | 8 | Contraste |
