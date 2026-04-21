# 🔬 Alnoms Demonstration Suite

This directory contains the **official runnable demonstrations** for the Alnoms Algorithmic Governance Engine.  
These scripts are **not unit tests** — they are **user‑facing examples** that illustrate:

- Static AST analysis  
- Anti‑pattern detection  
- Dynamic profiling  
- Empirical scaling  
- Metadata‑driven remediation  
- Decision Engine behavior  
- DSA showcase components  

Run any demo directly:

```bash
python <demo_file>.py
```
---
## 📁 Directory Structure

```Code
examples/
└── alnoms/
    ├── 1_cubic_matrix.py
    ├── 2_quadratic_duplicates.py
    ├── 3_nested_membership.py
    ├── 4_concat_in_loop.py
    ├── 5_list_extend_vs_append.py
    ├── 6_redundant_sort.py
    ├── 7_manual_bubble_sort.py
    ├── 8_linear_search_in_loop.py
    ├── 9_naive_find.py
    ├── 10_dfs_like_loop.py
    ├── 11_cycle_detection_manual.py
    ├── 12_execution_entrypoint.py
    ├── 13_decision_engine.py
    ├── 14_profiler.py
    ├── 15_data_generators.py
    ├── 16_data_reader.py
    ├── 17_dsa_showcase.py
    ├── 18_end_to_end_performance.py
    ├── 19_empirical_demo.py
    ├── DEMONSTRATIONS.md
    └── run_demos_1_to_12.py
```
---
## 🧩 Part 1 — Algorithmic Anti-Patterns (Demos 1–12)

These scripts generate **deliberately inefficient programs** used to test the performance engine. They are the canonical examples for static analysis and pattern detection.

| Demo | File | Focus |
| :--- | :--- | :--- |
| **1** | `1_cubic_matrix.py` | Triple-nested loops, cubic complexity detection. |
| **2** | `2_quadratic_duplicates.py` | Duplicate detection via nested loops. |
| **3** | `3_nested_membership.py` | Membership test inside loop → set conversion fix. |
| **4** | `4_concat_in_loop.py` | Inefficient string/list concatenation inside loops. |
| **5** | `5_list_extend_vs_append.py` | Extend vs append performance patterns. |
| **6** | `6_redundant_sort.py` | Sorting inside loops → hoisting recommendation. |
| **7** | `7_manual_bubble_sort.py` | Manual bubble sort detection. |
| **8** | `8_linear_search_in_loop.py` | Repeated linear search anti-pattern. |
| **9** | `9_naive_find.py` | Naive scanning patterns. |
| **10** | `10_dfs_like_loop.py` | DFS-like nested iteration. |
| **11** | `11_cycle_detection_manual.py` | Manual cycle detection logic. |
| **12** | `12_execution_entrypoint.py` | Example of a script with a `__main__` entrypoint. |

### Run all 1–12 demos:

```code
python run_demos_1_to_12.py
```

---
## 🧠 Part 2 — Core Engine Components (Demos 13–16)

These demos isolate the internal modules that power the performance engine.

### 13 — Decision Engine
File: `13_decision_engine.py`
Demonstrates how Alnoms maps:
* **detected patterns** → **cures**
* **cures** → **metadata registry entries**
* **metadata** → **implementation modules**

Useful for understanding the OSS performance mapping layer.

### 14 — Profiler
File: `14_profiler.py`
Demonstrates:
* **benchmarking**
* **doubling tests**
* **decorator profiling**
* **stress suite comparisons**

*This is the canonical example of the Alnoms Profiler.*

### 15 — Data Generators
File: `15_data_generators.py`
Shows how synthetic arrays and structured inputs are produced for:
* **profiling**
* **empirical scaling**
* **performance audits**

### 16 — Data Reader
File: `16_data_reader.py`
Demonstrates simple ingestion utilities for reading structured data.
---
## 🏗️ Part 3 — Integration & Performance (Demos 17–18)

### 17 — DSA Showcase
File: `17_dsa_showcase.py`
A lightweight demonstration of the DSA facade:
* **sorting**
* **searching**
* **pointer algorithms**
* **graph algorithms**

*This is not a teaching module — it is a capability sampler.*

### ⭐ 18 — End-to-End Performance (Flagship Demo)
File: `18_end_to_end_performance.py`
This is the primary demonstration of the Alnoms Performance Engine.
It performs a full audit:
* **Static AST analysis**
* **Pattern detection**
* **Dynamic profiling**
* **Empirical scaling**
* **Complexity estimation**
* **Performance verdict**
* **Narrative report**
* **Recommended cure**

**This is the demo you show to:**
* **reviewers**
* **collaborators**
* **customers**
* **academic readers**

### 📈 19 — Empirical Scaling Contract
File: `19_empirical_demo.py`  
A focused demonstration of how Alnoms proves Big-O complexity dynamically via the `data_gen(n)` hook. Highlights:
* The `data_gen(n)` contract for automated input scaling.
* Detection and verification of a hidden $O(N^3)$ matrix multiplication trap.
* Generating empirical evidence to validate static heuristics.

---
## 📝 Notes

* **These demos are not part of the test suite.**
* **They do not affect coverage.**
* **They are not executed in CI.**
* **They are user-facing examples for learning and exploration.**