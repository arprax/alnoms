<p align="center">
  <img src="https://raw.githubusercontent.com/arprax/alnoms/main/assets/logo.png" alt="Alnoms Logo" width="450"/>
</p>
# Alnoms — The Performance Intelligence Engine.

**Alnoms is the Performance Intelligence Engine for the Applied Data Intelligence era.  
It profiles, analyzes, and proves algorithmic performance before code reaches production.**

Built by **Arprax Lab**, Alnoms brings scientific rigor to modern software engineering by unifying profiling, static analysis, and algorithmic knowledge into a single, developer‑first framework. 

In an era where AI‑generated code, cloud costs, and complexity blowups are accelerating, Alnoms ensures that the code you ship is fast, safe, and mathematically justified. Alnoms goes beyond standard library utilities to provide a complete **Pre-Deployment Performance Intelligence System**—ensuring that the code you ship scales safely in production.

---

## 🎯 The Alnoms Mission
> *"Applied Data Intelligence requires more than just code—it requires proof."*

Software today is written faster than ever — but validated slower than ever.
Teams unknowingly ship:

* Hidden O(N²) loops
* Redundant sorts
* Inefficient membership checks
* Expensive calls inside hot paths
* AI‑generated code with silent complexity traps

These mistakes don’t show up in code review.
They show up in **production**, as latency spikes, cloud bills, and outages.

**Alnoms is the missing performance intelligence layer.**  
It brings algorithmic literacy back into engineering — automatically.

---
## 🔬 What Alnoms Is?
Alnoms is a Pre‑Deployment Algorithmic Performance Intelligence Engine that combines:

* Static Pattern Detection
* Empirical Profiling (OHPV2)
* Complexity Estimation
* Fix Recommendations
* A Canonical DSA Library
* A CLI for automated audits

It is the first open‑source system that tells you:

* Why your code is slow
* What pattern caused it
* How to fix it
* What the complexity proof looks like

This is algorithmic intelligence — not just profiling.

---
## ⚡ Quick Start: Catching a Silent Trap

Let's look at a real-life example. You have a script (`slow_script.py`) that cross-references data:

```python
def slow_membership_sum(arr):
    total = 0
    for x in arr:
        # 🚨 SILENT TRAP: Membership check inside a loop.
        # This creates a hidden O(N^2) time complexity.
        if x in arr:
            total += x
    return total
```
Run an automated algorithmic audit on your script:
```bash
alnoms analyze slow_script.py --deep --start-n 50 --rounds 4
```

**Example Output:**
```text
==================================================
 🔬 ALNOMS PERFORMANCE REPORT 
==================================================
File: slow_script.py
Timestamp (UTC): 2026-04-16T06:02:38.742138Z
Total Execution Time: 0.0086s

🧠 DETECTED INTENT:
   Membership test ('in arr') inside loop

🚨 STATIC ANALYSIS (Diagnostics & Remediation)
--------------------------------------------------
1. ⚠️ ISSUE: Membership test ('in arr') inside loop (Function: slow_membership_sum | Line: 7)
   📖 Explanation: Membership checks on lists inside loops are O(N). Convert to a set for O(1) lookups.
   💊 RECOMMENDED CURE: O(N) Optimization
   🏗️ IMPLEMENTATION: builtin.set
   🔐 ACCESS TIER: OSS
   ⏱️ Complexity Shift: O(N*M) → O(N + M)

   💡 HOW TO FIX:
   --- BEFORE ---
   |  for k in keys:
   |      if k in items:
   |          process(k)
   --- AFTER ---
   |  items_set = set(items)
   |  for k in keys:
   |      if k in items_set:
   |          process(k)

⏱️ DYNAMIC PROFILING (Top Execution Bottlenecks)
--------------------------------------------------
   1. slow_membership_sum() -> 7e-05s (0.86%)

📈 EMPIRICAL SCALING ANALYSIS: slow_membership_sum()
--------------------------------------------------
N          | Time (s)     | Ratio    | Est. Complexity
--------------------------------------------------
50         | 0.00001      | -        | Initial Round  
100        | 0.00002      | 3.42     | O(N^2)         
200        | 0.00008      | 3.65     | O(N^2)         
400        | 0.00030      | 3.91     | O(N^2)         

⚖️ VERDICT:
⚠️ WARNING: Function operates at O(N^2). Unsafe for large-scale workloads.

📌 ADDITIONAL CONTEXT
--------------------------------------------------
   The function may appear fast at small input sizes,
   but empirical scaling confirms the true asymptotic behavior.

🚀 EXPECTED IMPACT
--------------------------------------------------
   For N = 10,000:
     • O(N²) → ~100,000,000 operations
     • O(N)  → ~10,000 operations
   Estimated speedup: ~100× to ~1,000× depending on hardware.

🤖 CONFIDENCE
--------------------------------------------------
   High — static analysis and empirical scaling agree.

🔁 AFTER FIX (SIMULATED)
--------------------------------------------------
   Est. Complexity: O(N)
   Expected Behavior: Linear scaling with stable performance.
   Recommended Implementation:
       s = set(arr)
       for x in arr:
           if x in s:
               total += x

==================================================

```
> *This is algorithmic intelligence, not just profiling.*
---

## 📦 Installation
[![PyPI version](https://img.shields.io/pypi/v/alnoms.svg?color=FF6F00&logo=pypi&logoColor=white)](https://pypi.org/project/alnoms/)

```bash
# Core framework and CLI
pip install alnoms
```
---
## 📁 Project Structure

```text
alnoms/
├── core/        # Profiler, Analyzer, Decision Engine
├── patterns/    # Pattern detection rules
├── fixes/       # Optimization strategies
└── dsa/         # Algorithms & data structures
```
---
## ✨ Core Features

### 🛡️ 1. Pre-Deployment Performance CLI
Alnoms acts as an automated "Algorithmic Pharmacy," detecting O(N²) traps and mapping them directly to optimized DSA solutions before they merge to production.

```bash
# Run a static + dynamic profile on any script
alnoms analyze my_script.py

# Run a deep empirical scaling (Doubling Test)
alnoms analyze my_script.py --deep --start-n 50 --rounds 5
```
### 🧪 2. Empirical Profiling API
High-precision performance analysis with:

* GC control
* Warmup cycles
* Doubling test (OHPV2) for Big-O estimation

```python
from alnoms.core import Profiler, DataGenerator
from alnoms.dsa.algorithms.sorting import QuickSort

# 1. Initialize the industrial profiler
profiler = Profiler(mode="min", repeats=5)

# 2. Run an empirical doubling test
results = profiler.run_doubling_test(
    QuickSort.quick_sort,
    DataGenerator.random_array,
    start_n=500,
    rounds=5
)

# 3. Print the Big-O mathematical proof
profiler.print_analysis("Quick Sort", results)
```
### 🧠 3. Pattern Detection Engine
Detects real-world performance issues:

* Nested loops → O(N²)
* Inefficient membership checks
* High-frequency I/O
* Redundant sorting
* Expensive calls inside loops

### 🛠️ 4. Fix Recommendation System
For every issue, Alnoms suggests:

* Better algorithms
* Better data structures
* Complexity improvements

Example:

O(N²) → O(N log N) → O(N)

### 🗄️ 5. Algorithmic Knowledge Base
Built-in registry of:

* Algorithms
* Data structures
* Big-O complexity mappings
* Performance characteristics

---
## 📊 Performance Metrics & Complexity Canon

Alnoms ships with a built-in static analysis engine that identifies algorithmic anti-patterns. Below are the core metrics and severity levels evaluated by the OSS engine.

### ⏱️ Algorithmic Complexity
A snapshot of our canonical implementations located in `src/alnoms/dsa/`.

| Category | Algorithm | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Sorting** | `QuickSort` | O(N log N) average | O(log N) |
| **Sorting** | `MergeSort` | O(N log N) guaranteed| O(N) |
| **Sorting** | `BubbleSort` | O(N²) worst | O(1) |
| **Graph** | `DijkstraSP`| O(E log V) | O(V) |
| **Searching**| `BinarySearch` | O(log N) | O(1) |
| **Structures**| `SeparateChainingHashST`| O(1) average | O(N) |

### 🚨 Pattern Severity Levels

| Pattern ID | Severity | Why it Matters |
| :--- | :--- | :--- |
| `nested_loops` | **High** | Causes hidden quadratic or cubic blowups under load. |
| `expensive_calls` | **High** | Repeated heavy API/DB operations inside loops. |
| `high_freq_io` | **Medium** | Excessive disk or network I/O causing thread blocking. |
| `inefficient_membership`| **Medium** | O(N) list membership checks inside loops. |
| `inplace_concat` | **Low** | Repeated string/list concatenation overhead. |
| `redundant_sort` | **Low** | Sorting the same immutable dataset multiple times. |

### 💰 Estimated Cost Heuristics

| Pattern | Estimated Cost Impact |
| :--- | :--- |
| `nested_loops` | ~O(N²) growth curve |
| `expensive_calls` | ~10–100× slowdown depending on call |
| `high_freq_io` | ~5–20× slowdown due to I/O latency |
| `inefficient_membership`| ~O(N) per check |
| `inplace_concat` | ~O(N²) for repeated concatenation |
| `redundant_sort` | ~O(N log N) repeated |

---

## 🎓 Demonstrations & Pedagogy

Run real examples from the `examples/` directory:
* **Performance:** `python examples/18_end_to_end_performance.py`
* **DSA:** `python examples/17_dsa_showcase.py`

## 🌱 The Alnoms Philosophy
> *"Applied Data Intelligence requires proof, not assumptions."*

Alnoms is built on three principles:
1. **Zero Magic:** No hidden optimizations. Every algorithm is explicit and inspectable.
2. **Empirical Truth:** We don’t guess complexity—we measure it.
3. **Industrial Reliability:** Designed to work in real-world systems, not just academic examples.

## 🔗 Links

- 🐙 GitHub: https://github.com/arprax/alnoms  
- 📖 Docs: https://alnoms.com
- 
## 📝 Citation
If you use **Alnoms** in your research, please cite (ee the "Cite this repository" button on GitHub) it as:

**Software:**

```bibtex
@software{alnoms2026,
  author       = {Chowdhury, Tanmoy},
  title        = {Alnoms: A Performance Intelligence Engine for Computational Analysis},
  year         = {2026},
  version      = {0.1.0},
  url          = {https://alnoms.com},
  note         = {Available at https://github.com/arprax/alnoms}
}
```
---
## JOSS Submission Summary

Alnoms is a deterministic Python library for classical algorithms, data structures, and performance analysis.

It provides reproducible implementations with explicit complexity analysis, uniform documentation, and a structured architecture designed for benchmarking, profiling, and algorithmic performance evaluation.

The library is suitable for research, education, and tooling, offering a curated suite of algorithms and data structures with predictable behavior and clear pedagogical and analytical value.

---

**👤 Tanmoy Chowdhury** | Founder, Arprax  
*© 2026 Arprax Lab — A core division of Arprax dedicated to Applied Data Intelligence.*