# GCC C Code Analyzer (Python)

This code is a simple **Python-based analyzer** for C (GCC) source code. It extracts important details such as:

* Function definitions
* Function calls 
* Variables with their datatypes
* Inline functions

The goal is to understand code structure using **basic parsing techniques**.

## Features

* Detects all functions in a C file
* Identifies **inline functions**
* Extracts **variables with datatypes**
* Finds **function calls** inside each function
* Displays relationships between functions

## Technologies Used

* Python 
* Regular Expressions (`re` module)

## How to Run

1. Save your Python file (e.g., `gcc_analyzer.py`)
2. Prepare a C file (e.g., `test.c`)
3. Run the program:

```bash
python gcc_analyzer.py test.c
```

## Output


## Name

Developed as part of  **code analysis and parsing**.
