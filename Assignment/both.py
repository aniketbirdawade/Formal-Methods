import sys
import re
from collections import defaultdict

def tokenize_statements(source: str) -> list[str]:

    source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)
    source = re.sub(r'//[^\n]*', '', source)

    statements = []
    i = 0
    lines = source.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^[a-zA-Z_]\w*\s*=\s*.+;$', line):
            statements.append(line.rstrip(';').strip())
        
        elif re.match(r'^(if|while|for)\s*\(', line):
            cond = re.search(r'\((.+)\)', line)
            if cond:
                statements.append('COND: ' + cond.group(1).strip())
    return statements


class BasicBlock:
    def __init__(self, bid: int):
        self.id = bid
        self.stmts: list[str] = []
        self.successors: list[int] = []
        self.predecessors: list[int] = []
        
        self.gen: set[str] = set()
        self.kill: set[str] = set()
        self.in_set: set[str] = set()
        self.out_set: set[str] = set()
        
        self.rd_gen: set[str] = set()
        self.rd_kill: set[str] = set()
        self.rd_in: set[str] = set()
        self.rd_out: set[str] = set()
        
        self.lv_gen: set[str] = set()    
        self.lv_kill: set[str] = set()   
        self.lv_in: set[str] = set()
        self.lv_out: set[str] = set()
        
        self.vb_gen: set[str] = set()
        self.vb_kill: set[str] = set()
        self.vb_in: set[str] = set()
        self.vb_out: set[str] = set()

    def __repr__(self):
        return f"B{self.id}"


def build_cfg(statements: list[str]) -> tuple[dict[int, BasicBlock], int, int]:

    blocks: dict[int, BasicBlock] = {}

    entry = BasicBlock(0)
    blocks[0] = entry

    prev_id = 0
    for idx, stmt in enumerate(statements, start=1):
        blk = BasicBlock(idx)
        blk.stmts.append(stmt)
        blocks[idx] = blk

        blocks[prev_id].successors.append(idx)
        blk.predecessors.append(prev_id)
        prev_id = idx

    exit_id = len(statements) + 1
    exit_blk = BasicBlock(exit_id)
    blocks[exit_id] = exit_blk
    blocks[prev_id].successors.append(exit_id)
    exit_blk.predecessors.append(prev_id)

    return blocks, 0, exit_id


_BINOP = r'[+\-*/&|^%]|<<|>>'

def extract_expressions(stmt: str) -> set[str]:

    exprs = set()
    if stmt.startswith('COND:'):
        text = stmt[5:].strip()
    elif '=' in stmt:
        text = stmt.split('=', 1)[1].strip()
    else:
        return exprs

    pattern = re.compile(
        r'([a-zA-Z_]\w*|\d+)\s*(' + _BINOP + r')\s*([a-zA-Z_]\w*|\d+)'
    )
    for m in pattern.finditer(text):
        left, op, right = m.group(1), m.group(2), m.group(3)
        exprs.add(f"{left} {op} {right}")
    return exprs

def defined_var(stmt: str) -> str | None:
    
    if stmt.startswith('COND:'):
        return None
    m = re.match(r'^([a-zA-Z_]\w*)\s*=', stmt)
    return m.group(1) if m else None

def expressions_using(var: str, all_exprs: set[str]) -> set[str]:
    """Return all expressions that contain the given variable."""
    pattern = re.compile(r'\b' + re.escape(var) + r'\b')
    return {e for e in all_exprs if pattern.search(e)}

def compute_gen_kill(blocks: dict[int, BasicBlock], all_exprs: set[str]):
    for blk in blocks.values():
        local_gen: set[str] = set()
        local_kill: set[str] = set()

        for stmt in blk.stmts:
            generated = extract_expressions(stmt)
            var = defined_var(stmt)

            local_gen |= (generated - local_kill)

            if var:
                killed = expressions_using(var, all_exprs)
                local_kill |= killed
                local_gen -= expressions_using(var, local_gen)

        blk.gen = local_gen
        blk.kill = local_kill

def solve_available_expressions(
    blocks: dict[int, BasicBlock],
    entry_id: int,
    exit_id: int,
    all_exprs: set[str]
):
    blocks[entry_id].out_set = set()
    for bid, blk in blocks.items():
        if bid != entry_id:
            blk.out_set = set(all_exprs)

    changed = True
    iteration = 0
    while changed:
        changed = False
        iteration += 1
        for bid in sorted(blocks.keys()):
            if bid == entry_id:
                continue
            blk = blocks[bid]

            if blk.predecessors:
                new_in = None
                for pred_id in blk.predecessors:
                    pred_out = blocks[pred_id].out_set
                    new_in = pred_out if new_in is None else new_in & pred_out
                new_in = new_in if new_in is not None else set()
            else:
                new_in = set()

            new_out = blk.gen | (new_in - blk.kill)

            if new_in != blk.in_set or new_out != blk.out_set:
                blk.in_set = new_in
                blk.out_set = new_out
                changed = True

    return iteration

def rd_compute_gen_kill(blocks: dict[int, BasicBlock],
                        all_defs: dict[str, list[str]]) -> None:
    for blk in blocks.values():
        local_gen: set[str] = set()
        local_kill: set[str] = set()

        for stmt in blk.stmts:
            var = defined_var(stmt)
            if var and var in all_defs:
                this_def = next(
                    (d for d in all_defs[var] if d.split(': ', 1)[1] == stmt),
                    None
                )
                if this_def:
                    local_gen = {d for d in local_gen
                                 if not d.startswith(tuple(
                                     x.split(':')[0] + ':'
                                     for x in all_defs[var]
                                 ))}
                    local_gen.add(this_def)
                    local_kill |= {d for d in all_defs[var] if d != this_def}

        blk.rd_gen  = local_gen
        blk.rd_kill = local_kill

def solve_reaching_definitions(
    blocks: dict[int, BasicBlock],
    entry_id: int
) -> int:
    for blk in blocks.values():
        blk.rd_in  = set()
        blk.rd_out = set()

    changed = True
    iteration = 0
    while changed:
        changed = False
        iteration += 1
        for bid in sorted(blocks.keys()):
            if bid == entry_id:
                continue
            blk = blocks[bid]

            new_in = set()
            for pid in blk.predecessors:
                new_in |= blocks[pid].rd_out

            new_out = blk.rd_gen | (new_in - blk.rd_kill)

            if new_in != blk.rd_in or new_out != blk.rd_out:
                blk.rd_in  = new_in
                blk.rd_out = new_out
                changed = True

    return iteration

def used_vars(stmt: str) -> set[str]:
    if stmt.startswith('COND:'):
        text = stmt[5:].strip()
    elif '=' in stmt:
        text = stmt.split('=', 1)[1].strip()
    else:
        return set()
    tokens = re.findall(r'\b([a-zA-Z_]\w*)\b', text)
    keywords = {'if', 'else', 'while', 'for', 'return', 'int', 'float',
                'char', 'double', 'void', 'long', 'short', 'unsigned'}
    return {t for t in tokens if t not in keywords}

def lv_compute_gen_kill(blocks: dict[int, BasicBlock]) -> None:
    for blk in blocks.values():
        ue_var: set[str] = set()
        var_kill: set[str] = set()

        for stmt in blk.stmts:
            used = used_vars(stmt)
            var  = defined_var(stmt)
            ue_var |= (used - var_kill)
            if var:
                var_kill.add(var)

        blk.lv_gen  = ue_var
        blk.lv_kill = var_kill

def solve_live_variables(
    blocks: dict[int, BasicBlock],
    exit_id: int
) -> int:
    for blk in blocks.values():
        blk.lv_in  = set()
        blk.lv_out = set()

    changed = True
    iteration = 0
    while changed:
        changed = False
        iteration += 1
        
        for bid in sorted(blocks.keys(), reverse=True):
            if bid == exit_id:
                continue
            blk = blocks[bid]

            new_out = set()
            for sid in blk.successors:
                new_out |= blocks[sid].lv_in

            new_in = blk.lv_gen | (new_out - blk.lv_kill)

            if new_out != blk.lv_out or new_in != blk.lv_in:
                blk.lv_out = new_out
                blk.lv_in  = new_in
                changed = True

    return iteration

def vb_compute_gen_kill(blocks: dict[int, BasicBlock],
                        all_exprs: set[str]) -> None:
    for blk in blocks.values():
        local_gen: set[str] = set()
        local_kill: set[str] = set()

        for stmt in blk.stmts:
            generated = extract_expressions(stmt)
            var = defined_var(stmt)

            local_gen |= (generated - local_kill)

            if var:
                killed = expressions_using(var, all_exprs)
                local_kill |= killed

                local_gen -= expressions_using(var, local_gen)

        blk.vb_gen  = local_gen
        blk.vb_kill = local_kill

def solve_very_busy_expressions(
    blocks: dict[int, BasicBlock],
    entry_id: int,
    exit_id: int,
    all_exprs: set[str]
) -> int:

    for bid, blk in blocks.items():
        blk.vb_in  = set(all_exprs)
        blk.vb_out = set(all_exprs)

    blocks[exit_id].vb_in  = set()
    blocks[exit_id].vb_out = set()

    changed = True
    iteration = 0
    while changed:
        changed = False
        iteration += 1

        for bid in sorted(blocks.keys(), reverse=True):
            if bid == exit_id:
                continue
            blk = blocks[bid]

            new_out = None
            for sid in blk.successors:
                s_in = blocks[sid].vb_in
                new_out = s_in if new_out is None else new_out & s_in
            new_out = new_out if new_out is not None else set()

            new_in = blk.vb_gen | (new_out - blk.vb_kill)

            if new_out != blk.vb_out or new_in != blk.vb_in:
                blk.vb_out = new_out
                blk.vb_in  = new_in
                changed = True

    return iteration

def fmt_set(s: set[str]) -> str:
    if not s:
        return "∅"
    return "{ " + ",  ".join(sorted(s)) + " }"


def print_results(
    blocks: dict[int, BasicBlock],
    entry_id: int,
    exit_id: int,
    ae_iters: int,
    rd_iters: int,
    lv_iters: int,
    vb_iters: int,
    filename: str
):
    ordered = sorted(blocks.keys())

    def blk_label(bid):
        if bid == entry_id: return "ENTRY"
        if bid == exit_id:  return "EXIT"
        return f"{bid}"

    print(f"  ANALYSIS 1 — AVAILABLE EXPRESSIONS")

    print("\nGEN and KILL Sets")
    print(f"  {'State':<10} | {'GEN { }':<28} | {'KILL { }':<28}")
    print(f"  {'-'*50}")
    for bid in ordered:
        blk  = blocks[bid]
        lbl  = blk_label(bid)
        gen  = fmt_set(blk.gen)
        kill = fmt_set(blk.kill)
        print(f"  {lbl:<10} | {gen:<28} | {kill:<28}")
    print(f"  {'-'*50}")

    print("\nAEntry")
    print(f"  {'-'*50}")
    for idx, bid in enumerate(ordered, start=1):
        blk = blocks[bid]
        lbl = blk_label(bid)
        print(f"  AEntry({idx:<2})  [{lbl:<6}]  =  {fmt_set(blk.in_set)}")
    print(f"  {'-'*50}")

    print("\nAExit")
    print(f"  {'-'*50}")
    for idx, bid in enumerate(ordered, start=1):
        blk = blocks[bid]
        lbl = blk_label(bid)
        print(f"  AExit ({idx:<2})  [{lbl:<6}]  =  {fmt_set(blk.out_set)}")
    print(f"  {'-'*50}")

    print(f"  ANALYSIS 2 — REACHING DEFINITIONS")

    print("\nGEN and KILL Sets")
    print(f"  {'State':<10} | {'GEN { }':<28} | {'KILL { }':<28}")
    print(f"  {'-'*50}")
    for bid in ordered:
        blk  = blocks[bid]
        lbl  = blk_label(bid)
        gen  = fmt_set(blk.rd_gen)
        kill = fmt_set(blk.rd_kill)
        print(f"  {lbl:<10} | {gen:<28} | {kill:<28}")
    print(f"  {'-'*50}")

    print("\nRDEntry")
    print(f"  {'-'*50}")
    for idx, bid in enumerate(ordered, start=1):
        blk = blocks[bid]
        lbl = blk_label(bid)
        print(f"  RDEntry({idx:<2})  [{lbl:<6}]  =  {fmt_set(blk.rd_in)}")
    print(f"  {'-'*50}")

    print("\nRDExit")
    print(f"  {'-'*50}")
    for idx, bid in enumerate(ordered, start=1):
        blk = blocks[bid]
        lbl = blk_label(bid)
        print(f"  RDExit ({idx:<2})  [{lbl:<6}]  =  {fmt_set(blk.rd_out)}")
    print(f"  {'-'*50}")

    print(f"  ANALYSIS 3 — LIVE VARIABLES")

    print("\nGEN and KILL Sets")
    print(f"  {'State':<10} | {'GEN { }':<28} | {'KILL { }':<28}")
    print(f"  {'-'*50}")
    for bid in ordered:
        blk  = blocks[bid]
        lbl  = blk_label(bid)
        gen  = fmt_set(blk.lv_gen)
        kill = fmt_set(blk.lv_kill)
        print(f"  {lbl:<10} | {gen:<28} | {kill:<28}")
    print(f"  {'-'*50}")

    print("\nLVEntry")
    print(f"  {'-'*50}")
    for idx, bid in enumerate(ordered, start=1):
        blk = blocks[bid]
        lbl = blk_label(bid)
        print(f"  LVEntry({idx:<2})  [{lbl:<6}]  =  {fmt_set(blk.lv_in)}")
    print(f"  {'-'*50}")

    print("\nLVExit")
    print(f"  {'-'*50}")
    for idx, bid in enumerate(ordered, start=1):
        blk = blocks[bid]
        lbl = blk_label(bid)
        print(f"  LVExit ({idx:<2})  [{lbl:<6}]  =  {fmt_set(blk.lv_out)}")
    print(f"  {'-'*50}")

    print(f"  ANALYSIS 4 — VERY BUSY EXPRESSIONS")

    print("\nGEN and KILL Sets")
    print(f"  {'State':<10} | {'GEN { }':<28} | {'KILL { }':<28}")
    print(f"  {'-'*50}")
    for bid in ordered:
        blk  = blocks[bid]
        lbl  = blk_label(bid)
        gen  = fmt_set(blk.vb_gen)
        kill = fmt_set(blk.vb_kill)
        print(f"  {lbl:<10} | {gen:<28} | {kill:<28}")
    print(f"  {'-'*50}")

    print("\nVBEntry")
    print(f"  {'-'*50}")
    for idx, bid in enumerate(ordered, start=1):
        blk = blocks[bid]
        lbl = blk_label(bid)
        print(f"  VBEntry({idx:<2})  [{lbl:<6}]  =  {fmt_set(blk.vb_in)}")
    print(f"  {'-'*50}")

    print("\nVBExit")
    print(f"  {'-'*50}")
    for idx, bid in enumerate(ordered, start=1):
        blk = blocks[bid]
        lbl = blk_label(bid)
        print(f"  VBExit ({idx:<2})  [{lbl:<6}]  =  {fmt_set(blk.vb_out)}")
    print(f"  {'-'*50}")
    print()

def analyse(filepath: str):
    try:
        with open(filepath, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)

    stmts = tokenize_statements(source)
    if not stmts:
        print("[WARNING] No analysable statements found in the file.")
        sys.exit(0)

    all_exprs: set[str] = set()
    for s in stmts:
        all_exprs |= extract_expressions(s)

    all_defs: dict[str, list[str]] = {}
    def_counter = 1
    for s in stmts:
        var = defined_var(s)
        if var:
            lbl = f"d{def_counter}: {s}"
            def_counter += 1
            all_defs.setdefault(var, []).append(lbl)

    
    blocks, entry_id, exit_id = build_cfg(stmts)

    compute_gen_kill(blocks, all_exprs)
    ae_iters = solve_available_expressions(blocks, entry_id, exit_id, all_exprs)

    rd_compute_gen_kill(blocks, all_defs)
    rd_iters = solve_reaching_definitions(blocks, entry_id)

    lv_compute_gen_kill(blocks)
    lv_iters = solve_live_variables(blocks, exit_id)

    vb_compute_gen_kill(blocks, all_exprs)
    vb_iters = solve_very_busy_expressions(blocks, entry_id, exit_id, all_exprs)

    print_results(blocks, entry_id, exit_id, ae_iters, rd_iters, lv_iters, vb_iters, filepath)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python available_reaching.py <file.c>")
        sys.exit(1)
    analyse(sys.argv[1])