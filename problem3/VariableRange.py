import re

class VariableRangePass:

    def __init__(self):
        self.ranges = {}

    def update_range(self, var, low, high):
        self.ranges[var] = (low, high)

    def analyze(self, filename):

        with open(filename, "r") as f:
            lines = f.readlines()

        for lineno, line in enumerate(lines, start=1):

            line = line.strip()

            match = re.match(r'(\w+)\s*=\s*(\d+)\s*;', line)

            if match:
                var = match.group(1)
                value = int(match.group(2))

                self.update_range(var, value, value)

            match = re.search(r'if\s*\(\s*(\w+)\s*([<>]=?)\s*(\d+)\s*\)', line)

            if match:

                var = match.group(1)
                op = match.group(2)
                value = int(match.group(3))

                if op == ">":
                    self.update_range(var, value + 1, float("inf"))

                elif op == ">=":
                    self.update_range(var, value, float("inf"))

                elif op == "<":
                    self.update_range(var, float("-inf"), value - 1)

                elif op == "<=":
                    self.update_range(var, float("-inf"), value)

        print("Inferred Variable Ranges:\n")

        for var, (low, high) in self.ranges.items():

            low_str = str(low) if low != float("-inf") else "-∞"
            high_str = str(high) if high != float("inf") else "∞"

            print(f"{var} ∈ [{low_str}, {high_str}]")

        print("\nAnalysis Completed")


analyzer = VariableRangePass()
analyzer.analyze("sample.c")