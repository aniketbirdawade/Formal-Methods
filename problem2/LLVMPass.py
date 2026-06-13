import re

class ConstantStringDetector:

    def __init__(self):
        self.constant_strings = []

    def analyze(self, filename):

        with open(filename, "r") as file:
            lines = file.readlines()

        for lineno, line in enumerate(lines, start=1):

            strings = re.findall(r'"([^"]*)"', line)

            if strings:
                for s in strings:
                    print(f"Line {lineno}: Constant String Found : \"{s}\"")
                    self.constant_strings.append(s)

            if "=" in line and strings:
                print(f"Line {lineno}: String Assignment Detected")

            if any(func in line for func in ["printf", "puts", "fprintf"]):
                if strings:
                    print(f"Line {lineno}: String Usage Detected")

        print("\nTotal Constant Strings Found:",
            len(self.constant_strings))


detector = ConstantStringDetector()
detector.analyze("llmvPass.c")