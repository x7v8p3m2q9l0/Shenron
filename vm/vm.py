import dis
import textwrap
import random
import types
from .opcodes import OP_HANDLERS
import io
import tokenize
import marshal

def remove_comments(source: str) -> str:
    """Remove all # comments from Python source while keeping code intact."""
    out = []
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)  # works 3.7+
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            continue
        out.append(tok)
    return tokenize.untokenize(out)


def var_con_cak():
    return "".join(
        random.choices(
            [
                chr(i)
                for i in range(44032, 55204)
                if chr(i).isprintable() and chr(i).isidentifier()
            ],
            k=11,
        )
    )


def serialize_const(c):
    if isinstance(c, types.CodeType):
        return f"marshal.loads({repr(marshal.dumps(c))})"
    elif isinstance(c, (bytes, bytearray)):
        return c.hex()
    elif isinstance(c, (tuple, list)):
        return type(c)(serialize_const(x) for x in c)
    elif isinstance(c, (str, int, float, bool, type(None))):
        return c
    else:
        return repr(c)


def code_to_vm_instrs(code):
    instrs = []
    used_opcodes = set()
    for instr in dis.get_instructions(code):
        instrs.append((instr.opcode, instr.arg))
        used_opcodes.add(instr.opcode)
    return instrs, code.co_consts, code.co_names, code.co_varnames, used_opcodes


def main(
    func,
    random_opcodes=False,
    random_seed: int | None = None,
    random_opcodes_count: int = 2,
    debug=False,
):
    code = func.__code__
    instrs, consts, names, varnames, used_opcodes = code_to_vm_instrs(code)
    # safe_consts = [serialize_const(c) for c in consts]

    all_opcodes = set(int(k) for k in OP_HANDLERS.keys())
    if random_seed:
        random.seed(random_seed)
    if random_opcodes:
        extra = set(
            random.sample(
                sorted(all_opcodes - used_opcodes),
                min(random_opcodes_count, len(all_opcodes - used_opcodes)),
            )
        )
        used_opcodes = used_opcodes | extra
    old_used = used_opcodes
    needed = random.sample(used_opcodes, len(used_opcodes))
    handlers_code = f"            if opcode == {needed[0]}:{OP_HANDLERS[needed[0]]}\n"
    for op in needed[1:]:
        if op not in OP_HANDLERS:
            raise NotImplementedError(f"OPCODES: {old_used-all_opcodes}")
        try:
            handlers_code += (
                f"            elif opcode == {op}:{remove_comments(OP_HANDLERS[op])}\n"
            )
        except Exception as e:
            raise RuntimeError(f"Error processing opcode {dis.opname[op]}: {e}")
    vmname = var_con_cak()
    secondlmao = var_con_cak()
    # Build full program
    standalone_src = f"""\

class VMError(Exception):
    pass
class ZM:
    def __init__(self, debug=False):
        self.stack = []
        self.pc = 0
        self.debug = debug
        self.block_stack=[]
        self.locals=[]
        self.globals = {"{}"}

    def push(self, v):
        if self.debug: print("  push", v)
        self.stack.append(v)

    def pop(self):
        if not self.stack:
            raise VMError("pop from empty stack")
        v = self.stack.pop()
        if self.debug: print("  pop ->", v)
        return v

    def top(self):
        return self.stack[-1]

    def {secondlmao}(self, bytecode, consts, names, varnames, globals_):
        self.locals=[None]*len(varnames)
        self.stack.clear()
        self.pc = 0
        varnames = list(varnames)
        globals_ = dict(globals_)
        consts = list(consts)

        while self.pc < len(bytecode):
            opcode, oparg = bytecode[self.pc]
            if self.debug:
                print(f"[pc={{self.pc}}] opcode={{opcode}} arg={{oparg}}")
            self.pc += 1

            if False:
                pass
{handlers_code}
            else:
                raise VMError(f"Unimplemented opcode {{opcode}}")

        return None

consts = {[serialize_const(c) for c in consts]}
names = {repr(list(names))}
varnames = {repr(list(varnames))}
bytecode = {repr(instrs)}
{vmname} = ZM(debug={debug})
{vmname}.{secondlmao}(bytecode, consts, names, varnames, globals())
"""
    generated_code = textwrap.dedent(standalone_src)
    # print(generated_code)
    return generated_code


if __name__ == "__main__":
    script_code, script_file = 'print("Hello, World!")', "<vm.py>"

    # Compile the script to a code object
    compiled_code = compile(script_code, script_file, "exec")

    # Create a function from the code object
    import types

    func = types.FunctionType(compiled_code, {})
    vm_program = main(func)
    print(vm_program)
