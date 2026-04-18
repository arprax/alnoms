---
title: 'Alnoms: A Deterministic, Governance‑Ready Python Library for Algorithmic Complexity Analysis and Data Structure Instrumentation'
tags:
  - Python
  - algorithms
  - data structures
  - complexity analysis
  - static analysis
  - education
authors:
  - name: Tanmoy
    affiliation: 1
affiliations:
  - name: Independent Researcher, Nacogdoches, Texas, USA
    index: 1
date: 2026-04-17
---

# Summary

Alnoms is a Python library providing deterministic, textbook‑grade
implementations of classical algorithms and data structures, combined
with a static‑analysis engine that computes structural and operational
complexity. The library is designed for research, education, and
tooling—offering reproducible algorithmic behavior, consistent
governance‑grade documentation, and a modular architecture suitable for
experiments, benchmarking, and curriculum development.

The project emphasizes clarity, correctness, and reproducibility.
Algorithms are implemented with explicit complexity guarantees, uniform
Google‑style docstrings, and mkdocstrings‑compatible module
documentation. The library includes sorting algorithms, graph search and
shortest‑path algorithms, priority queues, symbol tables, and classical
data structures. Each implementation is deterministic and free of
side‑effects, enabling controlled experimentation and pedagogical use.

# Statement of Need

Researchers, educators, and students frequently require algorithmic
implementations that are:

1. **Deterministic** — predictable behavior for experiments and teaching  
2. **Governance‑consistent** — uniform documentation, structure, and
   complexity guarantees  
3. **Modular** — components usable independently or as part of larger
   analyses  
4. **Reproducible** — stable outputs for benchmarking and comparative
   studies  

Existing libraries (e.g., standard Python collections, ad‑hoc teaching
code, or performance‑oriented libraries) do not provide a unified,
documentation‑governed, complexity‑explicit suite of classical
algorithms suitable for research reproducibility. Alnoms fills this gap
by offering a curated, fully documented, and academically aligned
collection of algorithms and data structures.

# Functionality

Alnoms provides:

- **Sorting algorithms**: Merge Sort, Quick Sort, Heap Sort, Shell Sort,
  Insertion Sort, Selection Sort, Bubble Sort  
- **Graph algorithms**: BFS, DFS, Depth‑First Order, Dijkstra’s
  shortest‑paths, topological sorting  
- **Data structures**: stacks, queues, bags, priority queues, symbol
  tables, edge‑weighted digraphs, directed edges  
- **Static analysis utilities**: AST‑based complexity estimation,
  operation counting, and structural inspection  

All modules include:

- File‑level introductions  
- Google‑style docstrings  
- mkdocstrings compatibility  
- Explicit complexity guarantees  
- Deterministic behavior  

# Example Usage

```python
from alnoms.dsa.sorting import MergeSort
arr = [5, 2, 9, 1]
sorted_arr = MergeSort.merge_sort(arr)
```
```python
from alnoms.dsa.graphs import BreadthFirstPaths
bfs = BreadthFirstPaths(G, 0)
path = bfs.path_to(5)
```

# Acknowledgements
The project draws on classical algorithmic literature and standard
teaching patterns but is an original implementation and documentation
effort.

# References
See `paper.bib`.
