import dis
import textwrap
import random
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
    dis.opmap["JUMP_FORWARD"]: """ self.pc += oparg """,
    dis.opmap["POP_JUMP_IF_FALSE"]: """ val = self.pop(); if not val: self.pc = oparg """,
    dis.opmap["POP_JUMP_IF_TRUE"]: """ val = self.pop(); if val: self.pc = oparg """,
    dis.opmap["LOAD_NAME"]: """
            name = names[oparg] if isinstance(names, (list, tuple)) else oparg
            if isinstance(names, dict):
                if name in names:
                    self.push(names[name])
                elif name in globals_:
                    self.push(globals_[name])
                else:
                    raise VMError(f"LOAD_NAME: {name!r} not found")
            else:
                raise VMError("LOAD_NAME: unexpected names format")
    """,
    dis.opmap["STORE_NAME"]: """
            key = names[oparg] if isinstance(names, (list, tuple)) else oparg
            names[key] = self.pop()
    """,
    dis.opmap["LOAD_GLOBAL"]: """
            key = names[oparg] if isinstance(names, (list, tuple)) else oparg
            if key in globals_:
                self.push(globals_[key])
            else:
                raise VMError(f"LOAD_GLOBAL: {key!r} not found")
    """,
    dis.opmap["STORE_GLOBAL"]: """
            key = names[oparg] if isinstance(names, (list, tuple)) else oparg
            globals_[key] = self.pop()
    """,
    dis.opmap["CALL_FUNCTION"]: """
            argc = oparg if isinstance(oparg, int) else 0
            args = [self.pop() for _ in range(argc)][::-1]
            func = self.pop()
            if callable(func):
                res = func(*args)
                self.push(res)
            else:
                raise VMError(f"CALL_FUNCTION target {func!r} is not callable")
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
            # EXTENDED_ARG shifts into the next opcode's oparg
            self.extended_arg = (oparg << 8)
    """,
    dis.opmap["LOAD_METHOD"]: """
        # Load a method without binding it
        self.stack.append(self.get_method(oparg))
    """,

    dis.opmap["CALL_METHOD"]: """
        # Call the method that was just loaded
        method, args = self.stack.pop(), self.stack.pop()
        self.stack.append(method(*args))
    """,
    dis.opmap["CALL_FUNCTION_KW"] : """
        # Pop function
        func = self.stack.pop()
        # Pop keyword names tuple
        kw_names = self.stack.pop()
        # Pop positional and keyword arguments
        args = [self.stack.pop() for _ in range(oparg)]
        kwargs = {name: self.stack.pop() for name in reversed(kw_names)}
        # Call the function
        self.stack.append(func(*reversed(args), **kwargs))
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
    dis.opmap["LOAD_FAST"] : """
    # Push local variable at index oparg
    self.stack.append(self.fastlocals[oparg])
    """,



}


def main(func, out_filename="vm_program.py"):
    code = func.__code__
    instrs, consts, names, varnames, used_opcodes = code_to_vm_instrs(code)
    all_opcodes = set(int(k) for k in OP_HANDLERS.keys())
    extra = set(random.sample(sorted(all_opcodes - used_opcodes), 2))
    old_used=used_opcodes
    used_opcodes=used_opcodes|extra
    handlers_code = ""
    for op in random.sample(used_opcodes, len(used_opcodes)):
        if op not in OP_HANDLERS:
            raise NotImplementedError(f"OPCODES: {old_used}")
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
        names = dict(names)
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

# ---- Program data ----
consts = {repr(consts)}
names = {{}}
varnames = {repr(list(varnames))}
bytecode = {repr(instrs)}
vm = ZM(debug=True)
for i, v in enumerate(args):
    names[varnames[i]] = v
vm.run(bytecode, consts=consts, names=names, varnames=varnames, globals_=globals())
'''
    return textwrap.dedent(standalone_src)
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