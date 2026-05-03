<p align="center">
  <img src="https://raw.githubusercontent.com/arprax/alnoms/main/assets/logo.png" alt="Alnoms Logo" width="450"/>
</p>

# Alnoms — The Performance Intelligence Engine.

**Alnoms is the Performance Intelligence Engine for the Applied Data Intelligence era.  
It profiles, analyzes, and proves algorithmic performance before code reaches production.**

Built by [**Arprax**](https://arprax.com/), Alnoms brings scientific rigor to modern software engineering by unifying profiling, static analysis, and algorithmic knowledge into a single, developer‑first framework. 

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
"""Inefficient script used for the Alnoms demonstration."""

def slow_membership_sum(arr):
    total = 0
    for x in arr:
        # Intentional O(N^2) membership trap
        if x in arr:
            total += x
    return total

# Required for empirical scaling
def data_gen(n):
    return (list(range(n)),)

if __name__ == "__main__":
    data = list(range(200))
    print(slow_membership_sum(data))

```
Run an automated algorithmic audit on your script:
```bash
alnoms analyze slow_script.py --deep --start-n 10 --rounds 2
```

**Example Output:**
```text
==================================================
⚖️ PERFORMANCE REPORT
==================================================
File: examples/alnoms/scripts/slow_script.py
Timestamp (UTC): 2026-04-20T19:05:04.103523Z
Total Execution Time: 0.0143s

🧠 DETECTED INTENT:
   Membership test ('in arr') inside loop

🚨 STATIC ANALYSIS (Diagnostics & Suggestions)
--------------------------------------------------
1. ⚠️ ISSUE: Membership test ('in arr') inside loop (Function: slow_membership_sum | Line: 7)
   📖 Explanation: Membership checks on lists inside loops are O(N). Convert to a set for O(1) lookups.
   💊 RECOMMENDED OPTIMIZATION: O(N)
   🏗️ IMPLEMENTATION: alnoms.dsa.structures.separate_chaining_hash_st
   🔐 ACCESS TIER: OSS
   ⏱️ Complexity Shift: O(N*M) → O(N + M)

   💡 SUGGESTED FIX:
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
   1. slow_membership_sum() -> 8e-05s (0.56%)

📈 EMPIRICAL SCALING ANALYSIS: slow_membership_sum()
--------------------------------------------------
N          | Time (s)     | Ratio    | Est. Complexity
--------------------------------------------------
10         | 0.00000      | -        | Initial Round  
20         | 0.00000      | 2.33     | O(N)           

⚖️ VERDICT:
✅ PASSED: Function operates at O(N). Safe for scaling.

📌 CONTEXT
--------------------------------------------------
   Empirical scaling validates asymptotic behavior under increasing load.

🚀 EXPECTED IMPACT
--------------------------------------------------
   For N = 10,000:
     • O(N²) → ~100,000,000 operations
     • O(N)  → ~10,000 operations
   Estimated improvement: 100×–1000× depending on workload.

🤖 CONFIDENCE
--------------------------------------------------
   Medium — mixed signals between analysis methods.

🔁 AFTER OPTIMIZATION (SIMULATED)
--------------------------------------------------
   Expected Complexity: O(N)
   Behavior: Linear scaling with stable performance.
   Suggested Implementation:
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

**1. The Local Surgical Tool (`analyze`)** Designed for human eyes. Provides rich terminal tables, dynamic profiling, and deep empirical proofs for surgical investigation of a single file.
```bash
# Run a static + dynamic profile on any script
alnoms analyze my_script.py

# Run a deep empirical scaling (Doubling Test)
alnoms analyze my_script.py --deep --start-n 50 --rounds 5
```

**2. The CI/CD Robot (`ci`)** Designed for automated pipelines (like GitHub Actions). A headless, ultra-fast static analysis mode that scans multiple files instantly and outputs strict JSON. It enforces FinOps guardrails by intentionally failing builds that breach your Big-O thresholds.
```bash
# Scan multiple files and output pure JSON
alnoms ci auth.py database.py routes.py

# Block the PR/Build if quadratic complexity or worse is detected
alnoms ci src/*.py --fail-on "O(N^2)"
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
  url          = {https://alnoms.com},
  note         = {Available at https://github.com/arprax/alnoms}
}
```
---

👤 [**Tanmoy Chowdhury**](https://tanmoychowdhury.com/) | Founder, Arprax  
*© 2026 Arprax Lab — A core division of Arprax dedicated to Applied Data Intelligence.*