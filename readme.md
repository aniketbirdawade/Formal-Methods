# Compiler Design Mini Project
## Overview

This mini project demonstrates various Compiler Analysis and LLVM-inspired Passes implemented using Python. The project focuses on static code analysis, data flow analysis, optimization detection, loop analysis, and variable range inference using sample C programs as input.

---

# Project Structure

```text
MINIPROJECT
│
├── problem1
│   ├── Analysis.py
│   └── sample.c
│
├── problem2
│   ├── FunctionOptimization.py
│   ├── functionOptimization.c
│   ├── LLVMOptimization.py
│   ├── llvmOptimization.c
│   ├── LLVMPass.py
│   ├── llvmPass.c
│   ├── LoopDepth.py
│   └── loopDepth.c
│
└── problem3
    ├── VariableRange.py
    └── sample.c
```

# Requirements

* Python 3.x
* Any code editor (VS Code recommended)
* Command Prompt / Terminal

Verify Python installation:

```bash
python --version
```

---

# Problem 1: Traditional Data Flow Analysis

## Description

Implements classical compiler data flow analyses using Control Flow Graphs (CFG), GEN/KILL sets, and iterative fixed-point computation.

### Analyses Implemented

1. Reaching Definitions
2. Live Variable Analysis
3. Available Expressions
4. Very Busy Expressions

### Input File

```text
sample.c
```

### Run

```bash
cd problem1
python Analysis.py sample.c
```

### Output

Displays IN and OUT sets for:

* Reaching Definitions
* Live Variables
* Available Expressions
* Very Busy Expressions

---

# Problem 2: LLVM-Inspired Analysis Passes

---

## A. Constant String Detection Pass

### File

```text
LLVMPass.py
```

### Description

Detects assignments and usages of constant string literals in a program.

### Features

* Detect string literals
* Detect string assignments
* Detect string usages
* Report line numbers

### Input File

```text
llvmPass.c
```

### Run

```bash
cd problem2
python LLVMPass.py llvmPass.c
```

### Example Output

```text
Constant String Found: Hello LLVM
String Assignment Detected
String Usage Detected
```

---

## B. Loop Depth and Dependency Analysis

### File

```text
LoopDepth.py
```

### Description

Analyzes loop nesting depth and identifies loop-carried dependencies.

### Features

* Detect nested loops
* Calculate maximum loop depth
* Identify dependent variables

### Input File

```text
loopDepth.c
```

### Run

```bash
cd problem2
python LoopDepth.py loopDepth.c
```

### Example Output

```text
Maximum Loop Depth : 2

Loop-Carried Dependencies:
sum
```

---

## C. Function Optimization Analysis

### File

```text
FunctionOptimization.py
```

### Description

Identifies optimization opportunities for functions.

### Features

* Function inlining candidates
* Small function detection
* Dead functions
* Recursive functions

### Input File

```text
functionOptimization.c
```

### Run

```bash
cd problem2
python FunctionOptimization.py functionOptimization.c
```

### Example Output

```text
add : Candidate for Function Inlining
unused : Dead Function
factorial : Recursive Function
```

---

## D. Optimization Opportunity Analysis

### File

```text
LLVMOptimization.py
```

### Description

Inspects source code and reports potential optimization opportunities.

### Features

* Dead Code Detection
* Constant Folding Opportunities
* Redundant Instructions
* Unused Variables
* Unreachable Code Detection

### Input File

```text
llvmOptimization.c
```

### Run

```bash
cd problem2
python LLVMOptimization.py llvmOptimization.c
```

### Example Output

```text
Constant Folding Opportunity Found
Unused Variable Detected
Unreachable Code Found
```

---

# Problem 3: Variable Range Analysis

### File

```text
VariableRange.py
```

### Description

Implements interval analysis and abstract interpretation concepts to infer variable ranges.

### Features

* Constant assignment tracking
* Range inference
* Conditional analysis
* Interval propagation

### Examples

```text
a ∈ [0,20]
x ∈ [1,∞]
n ∈ [1,100]
```

### Input File

```text
sample.c
```

### Run

```bash
cd problem3
python VariableRange.py sample.c
```

### Example Output

```text
Inferred Variable Ranges

a ∈ [0,20]
x ∈ [1,∞]
n ∈ [1,100]
```

---

# How to Run the Project

Open terminal in the respective folder and execute:

```bash
python <python_file> <input_c_file>
```

Examples:

```bash
python Analysis.py sample.c

python LLVMPass.py llvmPass.c

python LoopDepth.py loopDepth.c

python FunctionOptimization.py functionOptimization.c

python LLVMOptimization.py llvmOptimization.c

python VariableRange.py sample.c
```
---

# Author
**Aniket Birdawade**

Compiler Design Mini Project
