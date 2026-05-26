import re

class ConstantStringDetector:

    def __init__(self):
        self.lines = []

    def read_file(self, file):

        with open(file) as f:

            for line in f:

                line = line.strip()

                if line:
                    self.lines.append(line)

    def detect_strings(self):

        print("\nConstant String Detection\n")

        found = False

        for i, line in enumerate(self.lines):

            strings = re.findall(r'"(.*?)"', line)

            if strings:

                found = True

                print(f"Line {i+1}: {line}")

                for s in strings:
                    print(f'  Constant String: "{s}"')

                print("-" * 40)

        if not found:
            print("No constant strings found.")

    def run(self, file):

        self.read_file(file)

        self.detect_strings()


detector = ConstantStringDetector()

detector.run("sample.c")