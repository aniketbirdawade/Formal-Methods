import re
import sys

data_types = ["int", "float", "double", "char", "long", "short", "void"]

skip = {"if", "for", "while", "switch", "return", "printf", "scanf"}


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def remove_comments(code):
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*', '', code)
    return code


def find_functions(code):
    pattern = re.compile(r'(inline\s+)?([\w\s\*]+?)\s+(\w+)\s*\(([^)]*)\)\s*\{')
    functions = []

    for m in pattern.finditer(code):
        name = m.group(3)
        if name in skip:
            continue

        functions.append({
            "name": name,
            "params": m.group(4),
            "inline": m.group(1) is not None,
            "body": code[m.end():code.find("}", m.end())]
        })

    return functions


def find_variables(text):
    variables = []

    for t in data_types:
        matches = re.findall(r'\b' + t + r'\s+(\w+)', text)
        for v in matches:
            variables.append((t, v))

    return variables


def find_calls(text, fname):
    calls = []
    matches = re.findall(r'(\w+)\s*\(', text)

    for m in matches:
        if m not in skip and m != fname:
            calls.append(m)

    return list(set(calls))


def analyze(file):
    code = remove_comments(read_file(file))
    functions = find_functions(code)

    for fn in functions:
        print("\nFunction:", fn["name"])

        if fn["inline"]:
            print("  -> inline function")

        vars_ = find_variables(fn["params"] + fn["body"])
        print("  Variables:", vars_)

        calls = find_calls(fn["body"], fn["name"])
        print("  Calls:", calls)


# run
if len(sys.argv) < 2:
    print("Usage: python file.py code.c")
else:
    analyze(sys.argv[1])
