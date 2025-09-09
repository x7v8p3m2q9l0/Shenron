import dis
import textwrap
import random
import types

def serialize_const(c):
    if isinstance(c, types.CodeType):
        # Don't dump raw code objects
        return f"<code:{c.co_name}@{c.co_firstlineno}>"
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

# TODO: ADD MORE OPCODES
OP_HANDLERS = {
        dis.opmap["BINARY_POWER"] : """
                    b = self.pop(); a = self.pop(); self.push(a ** b)
        """,
        dis.opmap["BINARY_MULTIPLY"] : """
                    b = self.pop(); a = self.pop(); self.push(a * b)
        """,
        dis.opmap["BINARY_MODULO"] : """
                    b = self.pop(); a = self.pop(); self.push(a % b)
        """,
        dis.opmap["BINARY_ADD"] : """
                    b = self.pop(); a = self.pop(); self.push(a + b)
        """,
        dis.opmap["BINARY_SUBTRACT"] : """
                    b = self.pop(); a = self.pop(); self.push(a - b)
        """,
        dis.opmap["BINARY_SUBSCR"] : """
                    key = self.pop(); obj = self.pop(); self.push(obj[key])
        """,
        dis.opmap["BINARY_FLOOR_DIVIDE"] : """
                    b = self.pop(); a = self.pop(); self.push(a // b)
        """,
        dis.opmap["BINARY_TRUE_DIVIDE"] : """
                    b = self.pop(); a = self.pop(); self.push(a / b)
        """,
        dis.opmap["INPLACE_FLOOR_DIVIDE"] : """
                    b = self.pop(); a = self.pop(); self.push(a // b)
        """,
        dis.opmap["INPLACE_TRUE_DIVIDE"] : """
                    b = self.pop(); a = self.pop(); self.push(a / b)
        """,
        dis.opmap["GET_LEN"] : """
                    a = self.pop(); self.push(len(a))
        """,
        dis.opmap["POP_TOP"]: """ self.pop() """,
        dis.opmap["LOAD_CONST"]: """ self.push(consts[oparg]) """,
        dis.opmap["LOAD_FAST"]: """ self.push(names[varnames[oparg]]) """,
        dis.opmap["STORE_FAST"]: """ names[varnames[oparg]] = self.pop() """,
        dis.opmap["RETURN_VALUE"]: """ return self.pop() """,
        dis.opmap["COMPARE_OP"]: """
                import dis
                b = self.pop(); a = self.pop()
                cmp = dis.cmp_op[oparg]
                if cmp == '<': self.push(a < b)
                elif cmp == '>': self.push(a > b)
                elif cmp == '==': self.push(a == b)
                elif cmp == '!=': self.push(a != b)
                elif cmp == '<=': self.push(a <= b)
                elif cmp == '>=': self.push(a >= b)
                else: raise VMError(f"Unsupported COMPARE_OP {cmp}")
        """,
        dis.opmap["POP_JUMP_IF_FALSE"]: """
                val = self.pop()
                if not val:
                    self.pc = oparg """,
        dis.opmap["POP_JUMP_IF_TRUE"]: """
                val = self.pop()
                if val: 
                    self.pc = oparg
        """,
        dis.opmap["LOAD_NAME"]: """
                import builtins
                if isinstance(names, (list, tuple)):
                    name = names[oparg]
                elif isinstance(names, dict):
                    name = oparg
                else:
                    raise VMError("LOAD_NAME: unexpected names format")

                if isinstance(names, dict) and name in names:
                    self.push(names[name])
                elif name in globals_:
                    self.push(globals_[name])
                elif hasattr(builtins, name):
                    self.push(getattr(builtins, name))
                else:
                    raise VMError(f"LOAD_NAME: {name!r} not found")
        """,



        dis.opmap["STORE_NAME"]: """
                if isinstance(names, (list, tuple)):
                    key = names[oparg]
                else:
                    key = oparg
                names[key] = self.pop()
        """,
        dis.opmap["LOAD_GLOBAL"]: """
                if isinstance(names, (list, tuple)):
                    key = names[oparg]
                else:
                    key = oparg
                if key in globals_:
                    self.push(globals_[key])
                else:
                    raise VMError(f"LOAD_GLOBAL: {key!r} not found")
        """,
        dis.opmap["STORE_GLOBAL"]: """
                if isinstance(names, (list, tuple)):
                    key = names[oparg]
                else:
                    key = oparg
                globals_[key] = self.pop()
        """,
        dis.opmap["CALL_FUNCTION"]: """
                argc = oparg
                args = [self.pop() for _ in range(argc)][::-1]
                func = self.pop()
                result = func(*args)
                self.push(result)
        """,


        # MAKE_FUNCTION (132)
        dis.opmap["MAKE_FUNCTION"] :"""
                    # oparg bits: 0x01 -> has default args, 0x02 -> has kwonly defaults,
                    # 0x04 -> has annotations, 0x08 -> has closure
                    flags = oparg if isinstance(oparg, int) else 0
                    fn_name = self.pop()
                    code_obj = self.pop()

                    defaults = self.pop() if (flags & 0x01) else None
                    kwdefaults = self.pop() if (flags & 0x02) else None
                    annotations = self.pop() if (flags & 0x04) else None
                    closure = self.pop() if (flags & 0x08) else None

                    import types
                    fn = types.FunctionType(code_obj, globals_,
                                            name=fn_name,
                                            argdefs=defaults,
                                            closure=closure)
                    if kwdefaults: fn.__kwdefaults__ = kwdefaults
                    if annotations: fn.__annotations__ = annotations

                    self.push(fn)
        """,
        # TODO: DO MORE JUNK SHIT FOR NOP OPCODE
        dis.opmap["NOP"] : """
                    pass
        """,
        dis.opmap["JUMP_FORWARD"] : """
                    self.pc += oparg
        """,
        dis.opmap["JUMP_IF_FALSE_OR_POP"] : """
                    val = self.top()
                    if not val:
                        self.pc = oparg
                    else:
                        self.pop()
        """,
        dis.opmap["JUMP_IF_TRUE_OR_POP"] : """
                    val = self.top()
                    if val:
                        self.pc = oparg
                    else:
                        self.pop()
        """,
        dis.opmap["JUMP_ABSOLUTE"] : """
                    self.pc = oparg
        """,
        dis.opmap["BUILD_TUPLE"] : """
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(tuple(items))
        """,
        dis.opmap["BUILD_LIST"] : """
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(list(items))
        """,
        dis.opmap["BUILD_SET"] : """
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(set(items))
        """,
        dis.opmap["BUILD_MAP"] : """
                    self.push({})
        """,
        dis.opmap["EXTENDED_ARG"] : """
                    opcode, oparg = bytecode[self.pc]
                    oparg = (self.extended_arg | (oparg if oparg is not None else 0))
                    self.extended_arg = 0
        """,
        dis.opmap["LOAD_METHOD"]: """
                    if isinstance(names, (list, tuple)):
                        name = names[oparg]
                    elif isinstance(names, dict):
                        name = oparg
                    else:
                        raise VMError("LOAD_METHOD: unexpected names format")

                    obj = self.pop()
                    method = getattr(obj, name)
                    self.push(method)
        """,


        dis.opmap["CALL_METHOD"]: """
                    argc = oparg
                    args = [self.pop() for _ in range(argc)][::-1]
                    method = self.pop()
                    self.push(method(*args))
        """,
        dis.opmap["CALL_FUNCTION_KW"]: """
                    keys = self.pop()  # tuple of keyword names
                    argc = oparg
                    args = [self.pop() for _ in range(argc)][::-1]
                    func = self.pop()
                    # last len(keys) args are keyword values
                    kw = {keys[i]: args[-len(keys)+i] for i in range(len(keys))}
                    posargs = args[:-len(keys)] if keys else args
                    result = func(*posargs, **kw)
                    self.push(result)
        """,

        dis.opmap["CALL_FUNCTION_EX"] : """
                    func = self.stack.pop()
                    args = self.stack.pop()
                    if oparg & 1:
                        kwargs = self.stack.pop()
                        self.stack.append(func(*args, **kwargs))
                    else:
                        self.stack.append(func(*args))
        """,
        dis.opmap["SETUP_FINALLY"] : """
                    # Push the target of finally block onto block stack
                    self.block_stack.append(('finally', self.pc + oparg))
        """,
        dis.opmap["POP_BLOCK"]: """
                    # Pop a block from block stack (no value stack effect)
                    self.block_stack.pop()
        """,

        dis.opmap["POP_EXCEPT"]: """
                    # Pop exception handler (removes type, value, traceback)
                    self.stack.pop(); self.stack.pop(); self.stack.pop()
        """,

        dis.opmap["LOAD_ATTR"]: """
                    # Load attribute from object
                    if isinstance(names, (list, tuple)):
                        name = names[oparg]
                    elif isinstance(names, dict):
                        name = oparg
                    else:
                        raise VMError("LOAD_ATTR: unexpected names format")

                    obj = self.pop()
                    self.push(getattr(obj, name))
        """,

        dis.opmap["BUILD_CONST_KEY_MAP"]: """
                    keys = self.pop()  # tuple of keys
                    values = [self.pop() for _ in range(oparg)][::-1]
                    d = {keys[i]: values[i] for i in range(oparg)}
                    self.push(d)
        """,

}


def main(func, random_opcodes=False, random_seed:int|None=None, args=()):
    code = func.__code__
    instrs, consts, names, varnames, used_opcodes = code_to_vm_instrs(code)
    safe_consts=[serialize_const(c) for c in consts]

    all_opcodes = set(int(k) for k in OP_HANDLERS.keys())
    if random_seed:
        random.seed(random_seed)
    if random_opcodes:
        extra = set(random.sample(sorted(all_opcodes - used_opcodes), 2))
        used_opcodes=used_opcodes|extra
    old_used=used_opcodes
    needed=random.sample(used_opcodes, len(used_opcodes))
    handlers_code = f"            if opcode == {needed[0]}:{OP_HANDLERS[needed[0]]}\n"
    for op in needed[1:]:
        if op not in OP_HANDLERS:
            raise NotImplementedError(f"OPCODES: {old_used-all_opcodes}")
        handlers_code += f"            elif opcode == {op}:{OP_HANDLERS[op]}\n"
    
    # Build full program
    standalone_src = f'''\

class VMError(Exception):
    pass
class ZM:
    def __init__(self, debug=False):
        self.stack = []
        self.pc = 0
        self.debug = debug
        self.block_stack=[]

    def push(self, v):
        if self.debug: print("  push", v)
        self.stack.append(v)

    def pop(self):
        if not self.stack:
            raise VMError("pop from empty stack")
        v = self.stack.pop()
        if self.debug: print("  pop ->", v)
        return v

    def run(self, bytecode, consts, names, varnames, globals_):
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
args = {repr(list(args))}

consts = {[serialize_const(c) for c in consts]}
names = {repr(list(names))}
varnames = {repr(list(varnames))}
bytecode = {repr(instrs)}
vm = ZM()
# for i, v in enumerate(args):
#     names[varnames[i]] = v
vm.run(bytecode, consts=consts, names=names, varnames=varnames, globals_=globals())
'''
    generated_code = textwrap.dedent(standalone_src)
    # print(generated_code)
    return generated_code
if __name__ == "__main__":
    script_code, script_file = 'print("Hello, World!")', '<vm.py>'

    # Compile the script to a code object
    compiled_code = compile(script_code, script_file, 'exec')

    # Create a function from the code object
    import types
    func = types.FunctionType(compiled_code, {})

    # Generate the VM program
    vm_program = main(func)
    print(vm_program)