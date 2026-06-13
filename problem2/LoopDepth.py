import re

class LoopAnalyzer:

    def __init__(self):
        self.max_depth = 0
        self.current_depth = 0
        self.dependencies = set()

    def analyze(self, filename):

        with open(filename, "r") as f:
            lines = f.readlines()

        for lineno, line in enumerate(lines, start=1):

            line = line.strip()

            if re.search(r'\b(for|while)\b', line):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)

                print(f"Line {lineno}: Loop Found")
                print(f"Current Depth = {self.current_depth}")

            if "}" in line and self.current_depth > 0:
                self.current_depth -= 1

            match = re.search(r'(\w+)\s*=\s*(.*);', line)

            if match:
                lhs = match.group(1)
                rhs = match.group(2)

                vars_used = re.findall(r'\b[a-zA-Z_]\w*\b', rhs)

                if lhs in vars_used:
                    self.dependencies.add(lhs)

        print("Maximum Loop Depth :", self.max_depth)

        if self.dependencies:
            print("Loop-Carried Dependencies:")
            for var in self.dependencies:
                print(" -", var)
        else:
            print("No Loop-Carried Dependencies Detected")


analyzer = LoopAnalyzer()
analyzer.analyze("loopDepth.c")