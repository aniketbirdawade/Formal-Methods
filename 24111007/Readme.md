# Data Flow Analysis (DFA)

This code implements a simple **Data Flow Analysis (DFA)** tool using Python. It analyzes a given C program and computes important compiler design concepts:

* Reaching Definitions
* Live Variables
* Available Expressions
* Very Busy Expressions

## Features

* Reads input from a `.c` file
* Builds a simple Control Flow Graph (CFG)
* Performs 4 major data flow analyses:

  * Reaching Definitions
  * Live Variables
  * Available Expressions
  * Very Busy Expressions
* Prints **IN and OUT sets** for each statement

## Input Format

Create a file named `input.c` and write simple C-like statements:


## How to Run

### Step 1: Save the Python code

Save your code as:

```
Analysis.py
```

### Step 2: Create input file

Create:

```
sample.c
```

### Step 3: Run the program

```bash
python Analysis.py
```

---

##Output

The program prints results for each statement:

Example:

```
Reaching Definitions
s1: #include <stdio.h>
  IN : set()
  OUT: set()
s2: int main() {
  IN : set()
  OUT: set()
s3: int a, b, c, x, y, z;
  IN : set()
  OUT: set()
s4: a = 1;
  IN : set()
  OUT: {'d4'}
s5: b = 2;
  IN : {'d4'}
  OUT: {'d4', 'd5'}
s6: x = a + b;
  IN : {'d4', 'd5'}
  OUT: {'a b', 'd6', 'd4', 'd5'}
s7: y = a * b;
  IN : {'a b', 'd6', 'd4', 'd5'}
  OUT: {'d6', 'd5', 'a b', 'd7', 'd4'}
s8: a = 5;
  IN : {'d6', 'd5', 'a b', 'd7', 'd4'}
  OUT: {'d8', 'd6', 'd7', 'd5'}
s9: z = a + b;
  IN : {'d8', 'd6', 'd7', 'd5'}
  OUT: {'d6', 'd5', 'a b', 'd7', 'd8', 'd9'}
s10: c = x * y;
  IN : {'d6', 'd5', 'a b', 'd7', 'd8', 'd9'}
  OUT: {'x y', 'd6', 'd5', 'd10', 'a b', 'd7', 'd8', 'd9'}
s11: return 0;
  IN : {'x y', 'd6', 'd5', 'd10', 'a b', 'd7', 'd9', 'd8'}
  OUT: {'x y', 'd6', 'd5', 'd10', 'a b', 'd7', 'd9', 'd8'}
s12: }
  IN : {'x y', 'd6', 'd5', 'd10', 'a b', 'd7', 'd9', 'd8'}
  OUT: {'x y', 'd6', 'd5', 'd10', 'a b', 'd7', 'd9', 'd8'}

Live Variables
s1: #include <stdio.h>
  IN : set()
  OUT: set()
s2: int main() {
  IN : set()
  OUT: set()
s3: int a, b, c, x, y, z;
  IN : set()
  OUT: set()
s4: a = 1;
  IN : set()
  OUT: set()
s5: b = 2;
  IN : {'a'}
  OUT: {'b', 'a'}
s6: x = a + b;
  IN : {'b', 'a'}
  OUT: {'b', 'a', 'x'}
s7: y = a * b;
  IN : {'b', 'a', 'x'}
  OUT: {'y', 'b', 'x'}
s8: a = 5;
  IN : {'y', 'b', 'x'}
  OUT: {'x', 'a', 'y', 'b'}
s9: z = a + b;
  IN : {'x', 'a', 'y', 'b'}
  OUT: {'y', 'x'}
s10: c = x * y;
  IN : {'y', 'x'}
  OUT: set()
s11: return 0;
  IN : set()
  OUT: set()
s12: }
  IN : set()
  OUT: set()

Available Expressions
s1: #include <stdio.h>
  IN : {'x y', 'a b'}
  OUT: set()
s2: int main() {
  IN : {'x y', 'a b'}
  OUT: set()
s3: int a, b, c, x, y, z;
  IN : {'x y', 'a b'}
  OUT: set()
s4: a = 1;
  IN : {'x y', 'a b'}
  OUT: set()
s5: b = 2;
  IN : {'x y', 'a b'}
  OUT: set()
s6: x = a + b;
  IN : set()
  OUT: {'a b'}
s7: y = a * b;
  IN : {'a b'}
  OUT: {'a b'}
s8: a = 5;
  IN : {'x y', 'a b'}
  OUT: set()
s9: z = a + b;
  IN : set()
  OUT: {'a b'}
s10: c = x * y;
  IN : {'a b'}
  OUT: {'x y', 'a b'}
s11: return 0;
  IN : {'x y', 'a b'}
  OUT: {'x y', 'a b'}
s12: }
  IN : {'x y', 'a b'}
  OUT: {'x y', 'a b'}

Very Busy Expressions
s1: #include <stdio.h>
  IN : set()
  OUT: {'x y', 'a b'}
s2: int main() {
  IN : set()
  OUT: {'x y', 'a b'}
s3: int a, b, c, x, y, z;
  IN : set()
  OUT: {'x y', 'a b'}
s4: a = 1;
  IN : set()
  OUT: {'x y', 'a b'}
s5: b = 2;
  IN : set()
  OUT: {'x y', 'a b'}
s6: x = a + b;
  IN : {'a b'}
  OUT: {'a b'}
s7: y = a * b;
  IN : {'a b'}
  OUT: {'x y'}
s8: a = 5;
  IN : {'x y'}
  OUT: {'x y', 'a b'}
s9: z = a + b;
  IN : {'x y', 'a b'}
  OUT: {'x y'}
s10: c = x * y;
  IN : {'x y'}
  OUT: set()
s11: return 0;
  IN : set()
  OUT: {'x y', 'a b'}
s12: }
  IN : set()
  OUT: {'x y', 'a b'}
```

Each analysis shows:

* **IN set** → Data before execution
* **OUT set** → Data after execution

---

## Author

Developed for learning **Data Flow Analysis**

