import re

class OptimizationPass:

    def __init__(self):
        self.assigned = set()
        self.used = set()

    def analyze(self, filename):

        with open(filename, "r") as f:
            lines = f.readlines()

        unreachable = False

        for lineno, line in enumerate(lines, start=1):

            line = line.strip()

            if unreachable and line and line != "}":
                print(f"Line {lineno}: Unreachable Code : {line}")

            if "return" in line:
                unreachable = True

            match = re.search(r'(\w+)\s*=\s*(.*);', line)

            if match:

                lhs = match.group(1)
                rhs = match.group(2)

                self.assigned.add(lhs)

                const_expr = re.match(
                    r'^\s*(\d+)\s*([\+\-\*/])\s*(\d+)\s*$',
                    rhs
                )

                if const_expr:
                    print(f"Line {lineno}: Constant Folding Opportunity : {line}")

                if lhs in rhs:
                    print(f"Line {lineno}: Possible Redundant Instruction : {line}")

                vars_used = re.findall(r'\b[a-zA-Z_]\w*\b', rhs)

                for var in vars_used:
                    self.used.add(var)

        unused = self.assigned - self.used

        print("\nUnused Variables:")
        if unused:
            for var in unused:
                print(" -", var)
        else:
            print(" None")


optimizer = OptimizationPass()
optimizer.analyze("llvmOptimization.c")