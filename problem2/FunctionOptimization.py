import re

class FunctionOptimizationPass:

    def __init__(self):
        self.functions = {}
        self.calls = {}

    def analyze(self, filename):

        with open(filename, "r") as f:
            lines = f.readlines()

        current_function = None

        for line in lines:

            line = line.strip()

            match = re.match(
                r'(int|void|float|double|char)\s+(\w+)\s*\([^)]*\)\s*\{?',
                line
            )

            if match:
                current_function = match.group(2)
                self.functions[current_function] = 0
                self.calls[current_function] = []

            if current_function:
                self.functions[current_function] += 1

                call_matches = re.findall(r'(\w+)\s*\(', line)

                for call in call_matches:
                    if call not in ['if', 'for', 'while', 'switch', 'return']:
                        if call != current_function:
                            self.calls[current_function].append(call)

            if "}" in line:
                current_function = None

        for func, size in self.functions.items():

            if size <= 5:
                print(f"{func}: Candidate for Function Inlining")

        called = set()

        for c in self.calls.values():
            called.update(c)

        for func in self.functions:

            if func != "main" and func not in called:
                print(f"{func}: Dead Function")

        with open(filename, "r") as f:
            content = f.read()

        for func in self.functions:

            pattern = rf'\b{func}\s*\('

            occurrences = len(re.findall(pattern, content))

            if occurrences > 1:
                print(f"{func}: Possible Recursive Function")

optimizer = FunctionOptimizationPass()
optimizer.analyze("functionOptimization.c")