import dis
import textwrap
import random
import types
from .opcodes import OP_HANDLERS
import io
import tokenize
import marshal
import logging

# ---- helpers --------------------------------------------------------------
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
    # serialize constants into Python-literal-friendly values
    if isinstance(c, types.CodeType):
        return f"marshal.loads({repr(marshal.dumps(c))})"
    elif isinstance(c, (bytes, bytearray)):
        # return a bytes literal expression
        return repr(bytes(c))
    elif isinstance(c, (tuple, list)):
        # IMPORTANT: produce the same container type with serialized elements
        inner = ", ".join(repr(serialize_const(x)) for x in c)
        if isinstance(c, tuple):
            if len(c) == 1:
                return f"({inner},)"
            return f"({inner})"
        else:
            return f"[{inner}]"
    elif isinstance(c, (str, int, float, bool, type(None))):
        return repr(c)
    else:
        # fallback to a repr expression (may be unsafe for exotic objects)
        return repr(c)


def code_to_vm_instrs(code):
    instrs = []
    used_opcodes = set()
    for instr in dis.get_instructions(code):
        instrs.append((instr.opcode, instr.arg))
        used_opcodes.add(instr.opcode)
    return instrs, code.co_consts, code.co_names, code.co_varnames, used_opcodes


# ---- main generator -------------------------------------------------------
def main(
    func,
    random_opcodes=False,
    random_seed: int | None = None,
    random_opcodes_count: int = 2,
    debug=False,
):
    code = func.__code__
    instrs, consts, names, varnames, used_opcodes = code_to_vm_instrs(code)

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
    # make deterministic ordering for handler emission
    needed = list(random.sample(sorted(used_opcodes), len(used_opcodes)))

    # build handlers code
    handlers_code = ""
    first = True
    for op in needed:
        if op not in OP_HANDLERS:
            raise NotImplementedError(f"OPCODES: {old_used-all_opcodes}")
        try:
            snippet = remove_comments(OP_HANDLERS[op])
            if first:
                handlers_code += f"                if opcode == {op}:{snippet}\n"
                first = False
            else:
                handlers_code += f"                elif opcode == {op}:{snippet}\n"
        except Exception as e:
            raise RuntimeError(f"Error processing opcode {dis.opname[op]}: {e}")

    vmname = var_con_cak()
    secondlmao = var_con_cak()

    # Build full program (careful with indentation inside the triple-quoted string)
    standalone_src = f"""\
import logging, marshal

class VMError(Exception):
    pass

class ZM:
    def __init__(self, debug=False):
        # data stack
        self.stack = []
        # program counter
        self.pc = 0
        self.debug = debug
        # block stack for SETUP/POP handling
        self.block_stack = []
        # locals and globals will be dicts (populated per-run)
        self.locals = {{}}
        self.globals = None
        self.extended_arg = 0
        if self.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s [%(levelname)s] %(message)s",
                handlers=[
                    logging.FileHandler("app.log", encoding="utf-8"),
                ]
            )
    def push(self, v):
        if self.debug:
            logging.debug(f"  push {{v!r}}")
        self.stack.append(v)

    def pop(self):
        if not self.stack:
            raise VMError("pop from empty stack")
        v = self.stack.pop()
        if self.debug:
            logging.debug(f"  pop -> {{v!r}}")
        return v

    def top(self):
        if not self.stack:
            raise VMError("top from empty stack")
        return self.stack[-1]

    def pop_block(self):
        if not self.block_stack:
            raise VMError("POP_BLOCK on empty block stack")
        return self.block_stack.pop()

    def {secondlmao}(self, bytecode, consts, names, varnames, globals_):
        # initialize per-run state
        # varnames: a sequence of local variable names
        varnames = list(varnames)
        # locals as dict mapping varname -> None initially
        self.locals = {{name: None for name in varnames}}
        self.stack.clear()
        self.pc = 0
        # ensure we get a plain dict for globals
        globals_ = dict(globals_ or {{}})
        self.globals = globals_
        consts = list(consts)
        names = list(names)

        while self.pc < len(bytecode):
            opcode, oparg = bytecode[self.pc]
            if self.debug:
                logging.debug(f"[pc=self.pc] opcode={{opcode}} arg={{oparg}} block_stack={{self.block_stack}} stack_top={{self.stack[-6:]}}")
            self.pc += 1

            try:
                if False:
                    pass
{handlers_code}
                else:
                    raise VMError(f"Unimplemented opcode {{opcode}}")
            except Exception as exc:
                # handle with-exit blocks specially
                handled = False
                # iterate blocks from top -> bottom to find nearest 'with' handler
                while self.block_stack:
                    blk = self.block_stack.pop()
                    if blk.get("type") == "with":
                        exit_func = None
                        for cand in reversed(self.stack):
                            if callable(cand):
                                exit_func = cand
                                break
                        if exit_func is None:
                            # nothing to call — continue searching
                            continue

                        # Call exit_func(exc_type, exc_value, traceback)
                        exc_type = type(exc)
                        exc_val = exc
                        tb = getattr(exc, "__traceback__", None)
                        try:
                            suppress = exit_func(exc_type, exc_val, tb)
                        except Exception as e2:
                            raise

                        if suppress:
                            handled = True
                            break
                        else:
                            continue
                    else:
                        continue

                if not handled:
                    raise
                else:
                    continue
consts = [{', '.join(serialize_const(c) for c in consts)}]
names = {repr(list(names))}
varnames = {repr(list(varnames))}
bytecode = {repr(instrs)}
{vmname} = ZM(debug={debug})
# run the VM
{vmname}.{secondlmao}(bytecode, consts, names, varnames, globals())
"""
    generated_code = textwrap.dedent(standalone_src)
    return generated_code


# quick CLI test if run as script
if __name__ == "__main__":
    script_code, script_file = 'print("Hello, World!")', "<vm.py>"
    compiled_code = compile(script_code, script_file, "exec")
    import types
    func = types.FunctionType(compiled_code, {})
    vm_program = main(func)
    print(vm_program)
