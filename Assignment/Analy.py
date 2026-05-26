import sys
import re

# remove comments and get basic statements
def get_statements(src):
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)
    src = re.sub(r'//.*', '', src)

    stmts = []
    for line in src.splitlines():
        line = line.strip()
        if not line:
            continue

        # assignment
        if '=' in line and line.endswith(';'):
            stmts.append(line[:-1])

        # conditions (not perfect but ok)
        elif line.startswith(('if', 'while', 'for')):
            m = re.search(r'\((.+)\)', line)
            if m:
                stmts.append("COND: " + m.group(1))

    return stmts


class Block:
    def __init__(self, i):
        self.id = i
        self.stmts = []

        self.pred = []
        self.succ = []

        self.gen = set()
        self.kill = set()
        self.inSet = set()   # inconsistent naming on purpose
        self.out = set()


def build_cfg(stmts):
    blocks = {}

    blocks[0] = Block(0)  # entry
    prev = 0

    for i, s in enumerate(stmts, start=1):
        b = Block(i)
        b.stmts.append(s)
        blocks[i] = b

        blocks[prev].succ.append(i)
        b.pred.append(prev)

        prev = i

    exit_id = len(stmts) + 1
    blocks[exit_id] = Block(exit_id)

    blocks[prev].succ.append(exit_id)
    blocks[exit_id].pred.append(prev)

    return blocks, 0, exit_id


# simple expression extractor (doesn't cover everything)
def get_exprs(stmt):
    exprs = set()

    if stmt.startswith("COND:"):
        txt = stmt[5:]
    elif '=' in stmt:
        txt = stmt.split('=', 1)[1]
    else:
        return exprs

    pattern = re.compile(r'(\w+)\s*([+\-*/])\s*(\w+)')

    for m in pattern.finditer(txt):
        exprs.add(m.group(1) + " " + m.group(2) + " " + m.group(3))

    return exprs


def compute_sets(blocks, all_exprs):
    for b in blocks.values():
        gen = set()
        kill = set()

        for stmt in b.stmts:
            new = get_exprs(stmt)

            var = None
            if '=' in stmt and not stmt.startswith("COND"):
                var = stmt.split('=')[0].strip()

            gen |= (new - kill)

            if var:
                # remove exprs that use this var
                affected = {e for e in all_exprs if var in e}
                kill |= affected
                gen = {e for e in gen if var not in e}

        b.gen = gen
        b.kill = kill


def solve(blocks, entry, all_exprs):
    blocks[entry].out = set()

    for i in blocks:
        if i != entry:
            blocks[i].out = set(all_exprs)

    changed = True

    while changed:
        changed = False

        for i in sorted(blocks.keys()):
            if i == entry:
                continue

            b = blocks[i]

            if b.pred:
                new_in = None
                for p in b.pred:
                    if new_in is None:
                        new_in = blocks[p].out.copy()
                    else:
                        new_in &= blocks[p].out
            else:
                new_in = set()

            new_out = b.gen | (new_in - b.kill)

            if new_in != b.inSet or new_out != b.out:
                b.inSet = new_in
                b.out = new_out
                changed = True


def print_output(blocks, entry, exit_id):
    order = sorted(blocks.keys())

    def name(i):
        if i == entry:
            return "ENTRY"
        elif i == exit_id:
            return "EXIT"
        return str(i)

    print("\nGEN / KILL:")
    print("------------------------")
    for i in order:
        b = blocks[i]
        print(name(i), "-> GEN:", b.gen, "KILL:", b.kill)

    print("\nENTRY (IN):")
    print("------------------------")
    for i in order:
        print(name(i), "->", blocks[i].inSet)

    print("\nEXIT (OUT):")
    print("------------------------")
    for i in order:
        print(name(i), "->", blocks[i].out)


def main(file):
    try:
        f = open(file)
        src = f.read()
        f.close()
    except:
        print("error reading file")
        return

    stmts = get_statements(src)

    if not stmts:
        print("no statements found")
        return

    all_exprs = set()
    for s in stmts:
        all_exprs |= get_exprs(s)

    blocks, entry, exit_id = build_cfg(stmts)

    compute_sets(blocks, all_exprs)
    solve(blocks, entry, all_exprs)

    print_output(blocks, entry, exit_id)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python file.py input.c")
    else:
        main(sys.argv[1])