import re
from collections import defaultdict

class SimpleDFA:
    def __init__(self):
        self.lines = []
        self.graph = defaultdict(list)
        self.parents = defaultdict(list)

        self.defs = []
        self.use = []
        self.expr = []
        self.gen = []
        self.kill = []

    def read_file(self, file):
        with open(file) as f:
            for line in f:
                line = re.sub(r'//.*', '', line).strip()
                if line:
                    self.lines.append(line)

    def build_graph(self):
        n = len(self.lines)

        for i in range(n - 1):
            self.graph[i].append(i + 1)

        for u in self.graph:
            for v in self.graph[u]:
                self.parents[v].append(u)

    def analyze(self):
        for line in self.lines:

            if "=" in line:
                left, right = line.split("=")
                var = left.strip()

                # variables used
                tokens = re.findall(r'[a-zA-Z_]\w*', right)

                self.defs.append(var)
                self.use.append(set(tokens))

                # FIXED expression parsing
                expr_tokens = re.findall(r'[a-zA-Z_]\w*|\d+|\+|\-|\*|\/', right)

                if any(op in expr_tokens for op in ['+', '-', '*', '/']):
                    self.expr.append(" ".join(expr_tokens))
                else:
                    self.expr.append(None)

            else:
                self.defs.append(None)
                self.use.append(set())
                self.expr.append(None)

    def compute_gen_kill(self):

        all_expr = {e for e in self.expr if e}

        for i in range(len(self.lines)):

            gen = set()
            kill = set()

            if self.defs[i]:
                gen.add(f"d{i+1}")

            if self.expr[i]:
                gen.add(self.expr[i])

            # kill definitions
            for j in range(len(self.lines)):
                if i != j and self.defs[i] == self.defs[j]:
                    kill.add(f"d{j+1}")

            # FIXED safe variable matching
            if self.defs[i]:
                for e in all_expr:
                    tokens = re.findall(r'[a-zA-Z_]\w*', e)

                    if self.defs[i] in tokens:
                        kill.add(e)

            self.gen.append(gen)
            self.kill.append(kill)

    def reaching_def(self):

        n = len(self.lines)

        entry = [set() for _ in range(n)]
        exit = [set() for _ in range(n)]

        changed = True

        while changed:

            changed = False

            for i in range(n):
                new_entry = set()

                for p in self.parents[i]:
                    new_entry |= exit[p]

                new_exit = (new_entry - self.kill[i]) | self.gen[i]

                if new_exit != exit[i]:

                    entry[i] = new_entry
                    exit[i] = new_exit
                    changed = True

        return entry, exit

    def live_var(self):

        n = len(self.lines)

        entry = [set() for _ in range(n)]
        exit = [set() for _ in range(n)]

        changed = True

        while changed:
            changed = False

            for i in reversed(range(n)):
                new_exit = set()

                for s in self.graph[i]:
                    new_exit |= entry[s]

                d = {self.defs[i]} if self.defs[i] else set()

                new_entry = (new_exit - d) | self.use[i]

                if new_entry != entry[i]:

                    entry[i] = new_entry
                    exit[i] = new_exit

                    changed = True

        return entry, exit

    def available_expr(self):

        n = len(self.lines)

        entry = [set() for _ in range(n)]
        exit = [set() for _ in range(n)]

        all_expr = {e for e in self.expr if e}

        for i in range(n):
            entry[i] = all_expr.copy()

        changed = True

        while changed:

            changed = False

            for i in range(n):

                if self.parents[i]:          
                    new_entry = set.intersection(*(exit[p] for p in self.parents[i]))
                else:
                    new_entry = set()

                gen = {self.expr[i]} if self.expr[i] else set()

                # FIXED safe variable matching
                kill = set()

                if self.defs[i]:

                    for e in all_expr:

                        tokens = re.findall(r'[a-zA-Z_]\w*', e)

                        if self.defs[i] in tokens:
                            kill.add(e)

                new_exit = (new_entry - kill) | gen

                if new_exit != exit[i]:

                    entry[i] = new_entry
                    exit[i] = new_exit

                    changed = True

        return entry, exit

    def very_busy_expr(self):

        n = len(self.lines)

        entry = [set() for _ in range(n)]
        exit = [set() for _ in range(n)]

        all_expr = {e for e in self.expr if e}

        for i in range(n):
            exit[i] = all_expr.copy()

        changed = True

        while changed:
            changed = False
            for i in reversed(range(n)):

                if self.graph[i]:
                    new_exit = set.intersection(*(entry[s] for s in self.graph[i]))
                else:
                    new_exit = set()

                gen = {self.expr[i]} if self.expr[i] else set()

                # FIXED safe variable matching
                kill = set()

                if self.defs[i]:

                    for e in all_expr:
                        tokens = re.findall(r'[a-zA-Z_]\w*', e)
                        if self.defs[i] in tokens:
                            kill.add(e)

                new_entry = (new_exit - kill) | gen

                if new_entry != entry[i]:

                    entry[i] = new_entry
                    exit[i] = new_exit
                    changed = True

        return entry, exit

    def print_result(self, name, entry, exit):

        print(f"\n{name}")

        for i in range(len(self.lines)):

            print(f"s{i+1}: {self.lines[i]}")
            print("  IN :", entry[i])
            print("  OUT:", exit[i])

    def run(self, file):

        self.read_file(file)
        self.build_graph()
        self.analyze()
        self.compute_gen_kill()

        rd_in, rd_out = self.reaching_def()
        lv_in, lv_out = self.live_var()
        ae_in, ae_out = self.available_expr()
        vb_in, vb_out = self.very_busy_expr()

        self.print_result("Reaching Definitions", rd_in, rd_out)
        self.print_result("Live Variables", lv_in, lv_out)
        self.print_result("Available Expressions", ae_in, ae_out)
        self.print_result("Very Busy Expressions", vb_in, vb_out)

dfa = SimpleDFA()

dfa.run("sample.c")