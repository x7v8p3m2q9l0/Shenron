
class VMError(Exception):
    pass
class ZM:
    def __init__(self, debug=False):
        self.stack = []
        self.pc = 0
        self.debug = debug
        self.block_stack=[]
        self.locals=[]
        self.globals = {}

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

    def 렘따븖뼂뱋첰됩뜰쇓먍볯(self, bytecode, consts, names, varnames, globals_):
        self.locals=[None]*len(varnames)
        self.stack.clear()
        self.pc = 0
        varnames = list(varnames)
        globals_ = dict(globals_)
        consts = list(consts)

        while self.pc < len(bytecode):
            opcode, oparg = bytecode[self.pc]
            if self.debug:
                print(f"[pc={self.pc}] opcode={opcode} arg={oparg}")
            self.pc += 1

            if False:
                pass
            if opcode == 24:
                    b = self.pop(); a = self.pop(); self.push(a - b)

            elif opcode == 119:

                    exc = self.pop()
                    self.push(exc)
                    raise exc

            elif opcode == 101:
                    import builtins


                    if isinstance(names, (list, tuple)):
                        name = names[oparg]
                    elif isinstance(names, dict):                          
                        name = oparg
                    else:
                        raise VMError("LOAD_NAME: unexpected names format")


                    if hasattr(self, "locals") and name in self.locals:
                        self.push(self.locals[name])
                    elif name in self.globals:
                        self.push(self.globals[name])
                    elif hasattr(builtins, name):
                        self.push(getattr(builtins, name))
                    elif name in globals_:
                        self.push(globals_[name])
                    else:
                        raise NameError(f"name {name!r} is not defined")

            elif opcode == 83: return self.pop() 
            elif opcode == 100: self.push(consts[oparg]) 
            elif opcode == 9:
                    pass

            elif opcode == 113:
                    self.pc = oparg

            elif opcode == 105:

                    values = [self.pop() for _ in range(oparg)][::-1]                               
                    keys = self.pop()                          
                    if not isinstance(keys, (list, tuple)):
                        raise VMError("BUILD_MAP expects a tuple of keys")
                    d = {key: value for key, value in zip(keys, values)}
                    self.push(d)

            elif opcode == 4:
                    self.push(self.stack[-1])

            elif opcode == 144:
                    opcode, oparg = bytecode[self.pc]
                    oparg = (self.extended_arg | (oparg if oparg is not None else 0))
                    self.extended_arg = 0

            elif opcode == 156:
                    keys = self.pop()                         
                    values = [self.pop() for _ in range(oparg)][::-1]

                    for i in range(len(values)):
                        if isinstance(values[i], list) and len(values[i]) == 1:
                            values[i] = values[i][0]
                    d = dict(zip(keys, values))
                    self.push(d)

            elif opcode == 110:
                    self.pc += oparg

            elif opcode == 87:

                    self.block_stack.pop()

            elif opcode == 143:

                    manager = self.pop()
                    enter = manager.__enter__()
                    self.push(manager)
                    self.push(enter)

            elif opcode == 162:

                    iterable = self.pop()
                    target = self.stack[-1]
                    target.extend(iterable)

            elif opcode == 106:

                    if isinstance(names, (list, tuple)):
                        name = names[oparg]                  
                    elif isinstance(names, dict):
                        name = names.get(oparg)                            
                        if name is None:
                            raise VMError(f"LOAD_ATTR: invalid key {oparg}")
                    else:
                        raise VMError("LOAD_ATTR: unexpected names format")

                    obj = self.pop()
                    self.push(getattr(obj, name))

            elif opcode == 165:
                    mapping = self.pop()
                    target = self.stack[-1]
                    if not isinstance(target, dict):
                        raise VMError("DICT_UPDATE target not a dict")
                    target.update(mapping)

            elif opcode == 49:



                    exc = self.pop()
                    mgr = self.pop()
                    res = mgr.__exit__(*exc)
                    self.push(res)

            elif opcode == 155:

                    fmt_spec = None
                    if oparg & 0x04:
                        fmt_spec = self.pop()
                    val = self.pop()
                    if oparg & 0x03 == 0:                  
                        result = str(val)
                    elif oparg & 0x03 == 1:        
                        result = str(val)
                    elif oparg & 0x03 == 2:         
                        result = repr(val)
                    elif oparg & 0x03 == 3:          
                        result = ascii(val)
                    else:
                        raise VMError(f"FORMAT_VALUE: invalid conversion flag {oparg}")
                    if fmt_spec is not None:
                        result = format(result, fmt_spec)
                    self.push(result)

            elif opcode == 89:

                    self.stack.pop(); self.stack.pop(); self.stack.pop()

            elif opcode == 121:

                    exc_type = self.pop()
                    err = self.pop()
                    target = oparg
                    if not issubclass(err.__class__, exc_type):
                        self.pc = target

            elif opcode == 20:
                    b = self.pop(); a = self.pop(); self.push(a * b)

            elif opcode == 109:
                    name = names[oparg] if isinstance(names, (list, tuple)) else oparg
                    module = self.top()
                    self.push(getattr(module, name))

            elif opcode == 132:
                    flags = oparg if isinstance(oparg, int) else 0
                    fn_name = self.pop()
                    code_obj = self.pop()
                    defaults   = self.pop() if (flags & 0x01) else None
                    kwdefaults = self.pop() if (flags & 0x02) else None
                    annotations= self.pop() if (flags & 0x04) else None
                    closure    = self.pop() if (flags & 0x08) else None
                    import types, marshal, ast
                    def _codeobj_from_marshal_string(s):
                        prefix = "marshal.loads("
                        if not s.startswith(prefix) or not s.endswith(")"):
                            raise TypeError(f"String constant cannot be turned into code: {s!r}")
                        inner = s[len(prefix):-1]
                        code_bytes = ast.literal_eval(inner)
                        if not isinstance(code_bytes, (bytes, bytearray)):
                            raise TypeError("marshal.loads argument did not evaluate to bytes")
                        return marshal.loads(code_bytes)
                    if isinstance(code_obj, str):
                        code_obj = _codeobj_from_marshal_string(code_obj)
                    import types as _types
                    if not isinstance(code_obj, _types.CodeType):
                        raise TypeError(f"Expected code object for MAKE_FUNCTION, got {type(code_obj)}")
                    fn = types.FunctionType(code_obj, globals_)
                    if defaults is not None:
                        fn.__defaults__ = defaults
                    if kwdefaults is not None:
                        fn.__kwdefaults__ = kwdefaults
                    if annotations is not None:
                        if not isinstance(annotations, dict):
                            annotations = {}
                        fn.__annotations__ = annotations
                    if closure is not None:
                        fn.__closure__ = closure
                    try:
                        if isinstance(fn_name, str):
                            fn.__name__ = fn_name
                    except Exception:
                        pass
                    self.push(fn)

            elif opcode == 131:
                    argc = oparg
                    args = [self.pop() for _ in range(argc)][::-1]
                    func = self.pop()
                    result = func(*args)
                    self.push(result)

            elif opcode == 102:
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(tuple(items))

            elif opcode == 12:
                self.push(not self.pop())

            elif opcode == 141:
                    keys = self.pop()                          
                    argc = oparg
                    args = [self.pop() for _ in range(argc)][::-1]
                    func = self.pop()

                    kw = {keys[i]: args[-len(keys)+i] for i in range(len(keys))}
                    posargs = args[:-len(keys)] if keys else args
                    result = func(*posargs, **kw)
                    self.push(result)

            elif opcode == 108:
                    name = names[oparg] if isinstance(names, (list, tuple)) else oparg
                    fromlist = self.pop()
                    level    = self.pop()
                    module = __import__(name, globals_, names, fromlist, level)
                    self.push(module)

            elif opcode == 68:

                    iterable = self.pop()
                    self.push(iter(iterable))

            elif opcode == 157:

                    pieces = [self.pop() for _ in range(oparg)][::-1]
                    self.push(''.join(map(str, pieces)))

            elif opcode == 161:
                    argc = oparg
                    args = [self.pop() for _ in range(argc)][::-1]
                    method_info = self.pop()

                    method = None
                    if isinstance(method_info, tuple) and len(method_info) == 2:
                        obj, name = method_info
                        try:
                            method = getattr(obj, name)
                        except Exception:
                            self.push(None)
                            return
                    elif callable(method_info):
                        method = method_info
                    else:
                        self.push(None)
                        return


                    try:
                        args = [a.encode("utf-8") if isinstance(a, str) else a for a in args]
                        result = method(*args)
                    except AttributeError:
                        args = [a if isinstance(a, str) else a for a in args]
                        result = method(*args)
                    except Exception as e:
                        print(e)
                        result=None
                    self.push(result)

            elif opcode == 122:

                    self.block_stack.append(('finally', self.pc + oparg))

            elif opcode == 114:
                    val = self.pop()
                    if not val:
                        self.pc = oparg 
            elif opcode == 103:
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(list(items))

            elif opcode == 115:
                    val = self.pop()
                    if val: 
                        self.pc = oparg

            elif opcode == 145:

                    value = self.pop()
                    lst = self.stack[-oparg]
                    lst.append(value)

            elif opcode == 71:

                    self.push(__build_class__)

            elif opcode == 84:
                    module = self.pop()
                    for k, v in module.__dict__.items():
                        if not k.startswith("_"):
                            globals_[k] = v

            elif opcode == 1: self.pop() 
            elif opcode == 147:
                    value = self.pop()
                    key = self.pop()
                    mapping = self.pop()
                    mapping[key] = value
                    self.push(mapping)

            elif opcode == 23:
                    b = self.pop(); a = self.pop(); self.push(a + b)

            elif opcode == 90:

                    if isinstance(names, (list, tuple)):
                        key = names[oparg]
                    else:
                        key = str(oparg)

                    value = self.pop()
                    self.globals[key] = value

            elif opcode == 107:
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

            elif opcode == 160:
                    if isinstance(names, (list, tuple)):
                        name = names[oparg]
                    elif isinstance(names, dict):
                        name = oparg
                    else:
                        raise VMError("LOAD_METHOD: unexpected names format")

                    obj = self.pop()


                    self.push((obj, name))


            else:
                raise VMError(f"Unimplemented opcode {opcode}")

        return None

consts = [' ', '>> Running...', '\r', ('end',), 'sys', '<built-in function exit>', 'Hook hả con trai', '<built-in function print>', '<built-in function exec>', '<built-in function eval>', '<built-in function __import__>', '<built-in function input>', '<built-in function len>', 'marshal', '<built-in function loads>', 'Shenron', 'Nguyễn Xuân Trịnh', 'S_VM', 'Dragon Ball', 'https://t.me/CalceIsMe', 'https://www.youtube.com/watch?v=8yXEvIRFCwc&list=PLS0WF70AJy04pZ-OQwlsjuXiJL_3B9Oc4&index=4', ('Obfuscator', 'Obfuscator Owner', 'VM', 'Theme', 'Contact', 'Obfuscator Code Writing Process'), '⠀⠀⠀⠀⢨⠊⠀⢀⢀⠀⠀⠀⠈⠺⡵⡱⠀⠀⠀⢠⠃⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⢰⡁⠉⠊⠙⢎⣆⠀⠀⠀⠀⢩⢀⠜⠀⠀⠀\n⠀⠀⠀⢠⠃⠀⠀⢸⢸⡀⠀⠀⠀⠀⠘⢷⡡⠀⠀⠎⠀⢰⣧⠀⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠈⣐⢤⣀⣀⢙⠦⠀⠀⠀⠀⡇⠀⠀⠀⠀\n⠀⠀⢀⠃⠀⠀⠀⡌⢸⠃⠀⠀⠀⢀⠀⠀⠑⢧⡸⠀⢀⣿⢻⡀⠀⠀⣻⠀⠀⠀⠀⠀⣠⡴⠛⠉⠀⠀⠀⠑⢝⣦⠀⠀⠀⢰⠠⠁⠀⠀\n⠀⠀⠌⠀⠀⠀⡘⣖⣄⢃⠀⠀⠀⠈⢦⡀⠀⡜⡇⠀⣼⠃⠈⢷⣶⢿⠟⠀⠀⠀⢠⠞⠁⠀⣀⠄⠂⣶⣶⣦⠆⠋⠓⠀⢀⣀⡇⠀⠀⠀⠀⠀⠀\n⠡⡀⡇⠀⢰⣧⢱⠊⠘⡈⠄⠀⠀⡀⠘⣿⢦⣡⢡⢰⡇⢀⠤⠊⡡⠃⠀⠀⢀⡴⠁⢀⠔⠊⠀⠀⢠⣿⠟⠁⠀⢀⠀⢀⠾⣤⣀⠀⠀⡠\n⡀⠱⡇⠀⡆⢃⠀⠀⠀⠃⠀⠀⠀⣧⣀⣹⡄⠙⡾⡏⠀⡌⣠⡾⠁⠀⠀⣠⠊⢠⠔⠁⠀⠀⠀⠀⣸⡏⠀⠀⠀⢨⣪⡄⢻⣥⠫⡳⢊⣴\n⠀⠀⢡⢠⠀⢸⡆⠀⣀⠀⠀⠀⠀⠈⣛⢛⣁⣀⠘⣧⣀⢱⡿⠀⠀⢀⡔⢁⢔⠕⠉⠐⣄⣠⠤⠶⠛⠁⢀⣀⠀⠀⠉⠁⠈⠷⣞⠔⡕⣿\n⢄⡀⠘⢸⠀⣘⠇⠀⠀⠀⠀⠀⠀⠀⠀⠉⠐⠤⡑⢎⡉⢨⠁⠀⣠⢏⠔⠁⠘⣤⠴⢊⣡⣤⠴⠖⠒⠻⠧⣐⠓⠀⠀⠀⠀⠈⠀⡜⠀⠇\n⠤⡈⠑⠇⠡⣻⢠⠊⠉⠉⠉⠑⠒⠤⣀⠀⠀⠀⠈⣾⣄⢘⣫⣜⠮⢿⣆⡴⢊⢥⡪⠛⠉⠀⠀⠀⠀⢀⠄⠂⠁⠀⠀⠀⠀⠀⠀⢧⡀⠈\n⠁⠈⠑⠼⣀⣁⣇⠀⣴⡉⠉⠉⠀⠒⡢⠌⣐⡂⠶⣘⢾⡾⠿⢅⠀⣠⣶⡿⠓⠁⢠⠖⣦⡄⠀⠀⠀⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢎⢳\n⠀⠀⠀⠀⠉⣇⣿⢜⠙⢷⡄⠀⠀⠀⣄⣠⠼⢶⡛⣡⢴⠀⢀⠛⠱⡀⠀⠀⠀⠀⢀⠎⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡋⠮⡈\n⠀⠀⢀⣖⠂⢽⡈⠀⠈⠑⠻⡦⠖⢋⣁⡴⠴⠊⣉⡠⢻⡖⠪⢄⡀⢈⠆⠀⠀⢠⠊⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠤⡵⢤⣃\n⠀⠀⠸⢠⡯⣖⢵⡀⠀⠀⣠⣤⠮⠋⠁⠀⠀⠀⠀⠀⠸⣌⢆⢱⡾⠃⢀⠠⠔⠁⣀⢸⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⡸⠚⡸⠈⠁\n⠤⢀⣀⢇⢡⠸⡗⢔⡄⠸⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⡩⠔⢉⡠⠔⠂⠉⢀⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢁⠎⢀⡠⠔\n⠀⠀⠀⠘⡌⢦⡃⣎⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠠⡟⠠⡐⣋⠤⠀⣀⠤⠐⠂⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⢉⠉⠁⠀⠀\n⠤⠀⠀⠀⠰⡀⠈⠻⡤⠚⢄⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠈⠂⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⢸⠀⢀⠤⠊\n⣀⠀⠀⠀⠀⠘⠢⡑⢽⡬⢽⢆⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⡶⠟⣉⣉⢢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⠈⡖⠓⠒⠂\n⠀⢈⣑⣒⡤⠄⠀⠈⠑⠥⣈⠙⠧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣁⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⣠⡻⠀⠀⠀⠇⠐⡔⣡\n⠉⠉⠁⠀⠒⠒⠒⠒⠀⠤⠤⠍⣒⡗⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⠀⢠⡞⢡⠃⠀⠀⠀⢸⠀⠸⣡\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠈⣶⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠁⣠⡔⠉⠀⡎⠀⠀⠀⠀⢸⠀⠀⠃\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⣀⢼⠀⠀⠀⢉⡄⠈⠐⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⡜⡡⣾⠃⠀⠀⠸⠀⠀⠀⠀⠀⠀⡧⢄⡈\n⠀⠀⠀⠀⠀⠀⠀⣀⠤⠚⠉⠀⡆⠀⠀⠀⠈⡵⢄⡀⠀⠀⠙⠂⠄⣀⡀⠤⠊⠉⢀⣀⣠⡴⢿⣟⠞⠀⠀⢀⠇⠀⠀⠀⠀⠀⠀⡗⠢⢌\n⠀⠀⠀⠀⡠⠔⠉⠀⠀⢀⡠⡤⠇⠀⠀⢀⠀⠰⣣⠈⠐⠤⡀⠀⡀⠈⠙⢍⠉⣉⠤⠒⠉⣠⣟⢮⠂⡄⠀⣼⠁⠀⡆⠀⠀⠀⠀⢡⣀⠀\n⣿⡷⠖⠉⠀⠀⡠⠔⣪⣿⠟⣫⠀⠀⠀⢸⠀⠀⢩⢆⠀⠀⠈⠑⢳⠤⠄⠠⠭⠤⠐⠂⢉⣾⢮⠃⢠⠃⢰⡹⠀⢰⠀⠀⠀⠀⠀⢸⡉⣳\n⠉⠀⢀⡠⠒⠉⣠⠾⠋⢁⠔⠹⠀⠀⠀⡈⡇⠀⠀⢫⣆⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⣘⢾⠃⢀⠏⣠⡳⠁⠀⣾⠀⠀⠀⠀⠀⠀⠈⠉', 0, None, ('*',), ('minify_source',), ('var_con_cak',), ('main', 'remove_comments'), 99999999, '.', '>> Installing Module', 'os', 'pip', ' install pystyle', 'A', '🐉', 'B', '🐲', 'C', '⭐', 'D', '✦', 'E', '✧', 'F', '✨', 'G', '💫', 'H', '🌠', 'I', '⚡', 'J', '🔥', 'K', '💥', 'L', '☄', 'M', '️', 'N', '🌪', 'O', '❄', 'P', 'Q', '🌀', 'R', '🥋', 'S', '🥊', 'T', '⚔', 'U', 'V', '👊', 'W', '🙌', 'X', '👐', 'Y', '🟠', 'Z', '🔴', 'a', '🟡', 'b', '🟢', 'c', '🔵', 'd', '🟣', 'e', '⚫', 'f', '⚪', 'g', '👽', 'h', '🤖', 'i', '👺', 'j', '🐢', 'k', '🐒', 'l', '🦍', 'm', '👑', 'n', '💎', 'o', '🔮', 'p', '🍑', 'q', '🍗', 'r', '🍚', 's', '🍶', 't', '🏯', 'u', '⛩', 'v', '⛰', 'w', '🛡', 'x', 'y', '🧙', '\u200d', '♂', '🤜', '🤛', '😡', '😤', '🥵', '🤯', '🌌', '🌍', '🌑', '☀', ('z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/'), "marshal.loads(b'\\xe3\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x03\\x00\\x00\\x00\\x04\\x00\\x00\\x00C\\x00\\x00\\x00s\\x16\\x00\\x00\\x00i\\x00|\\x00]\\x07\\\\\\x02}\\x01}\\x02|\\x02|\\x01\\x93\\x02q\\x02S\\x00\\xa9\\x00r\\x01\\x00\\x00\\x00)\\x03\\xda\\x02.0\\xda\\x01k\\xda\\x01vr\\x01\\x00\\x00\\x00r\\x01\\x00\\x00\\x00\\xfa\\x05<SVM>\\xda\\n<dictcomp>+\\x00\\x00\\x00\\xf3\\x02\\x00\\x00\\x00\\x16\\x00')", '<dictcomp>', 'return', 'marshal.loads(b\'\\xe3\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x03\\x00\\x00\\x00\\x04\\x00\\x00\\x00C\\x00\\x00\\x00s,\\x00\\x00\\x00|\\x00\\xa0\\x00\\xa1\\x00\\xa0\\x01\\xa1\\x00}\\x01d\\x01\\xa0\\x02d\\x02d\\x03\\x84\\x00|\\x01D\\x00\\x83\\x01\\xa1\\x01}\\x02d\\x04|\\x02\\x9b\\x00d\\x05\\x9d\\x03S\\x00)\\x06N\\xda\\x00c\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x05\\x00\\x00\\x00s\\x00\\x00\\x00s\\x1c\\x00\\x00\\x00\\x81\\x00|\\x00]\\t}\\x01t\\x00\\xa0\\x01|\\x01|\\x01\\xa1\\x02V\\x00\\x01\\x00q\\x02d\\x00S\\x00\\xa9\\x01N)\\x02\\xda\\x01e\\xda\\x03get)\\x02\\xda\\x02.0\\xda\\x01c\\xa9\\x00r\\x07\\x00\\x00\\x00\\xfa\\x05<SVM>\\xda\\t<genexpr>/\\x00\\x00\\x00s\\x04\\x00\\x00\\x00\\x02\\x80\\x1a\\x00z\\x16enc.<locals>.<genexpr>z\\tshenron("z\\x02"))\\x03\\xda\\x06encode\\xda\\x03hex\\xda\\x04join)\\x03\\xda\\x01s\\xda\\x05noisy\\xda\\x06mappedr\\x07\\x00\\x00\\x00r\\x07\\x00\\x00\\x00r\\x08\\x00\\x00\\x00\\xda\\x03enc-\\x00\\x00\\x00s\\x06\\x00\\x00\\x00\\x0c\\x01\\x14\\x01\\x0c\\x01\')', 'enc', ('__import__', 'abs', 'all', 'any', 'ascii', 'bin', 'breakpoint', 'callable', 'chr', 'compile', 'delattr', 'dir', 'divmod', 'eval', 'exec', 'format', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'aiter', 'len', 'locals', 'max', 'min', 'next', 'anext', 'oct', 'ord', 'pow', 'print', 'repr', 'round', 'setattr', 'sorted', 'sum', 'vars', 'None', 'Ellipsis', 'NotImplemented', 'False', 'True', 'bool', 'memoryview', 'bytearray', 'bytes', 'classmethod', 'complex', 'dict', 'enumerate', 'filter', 'float', 'frozenset', 'property', 'int', 'list', 'map', 'object', 'range', 'reversed', 'set', 'slice', 'staticmethod', 'str', 'super', 'tuple', 'type', 'zip'), "\nprint(' ' * len('>> Running...'), end='\\r')\n\nif str(capsule_add('sys').exit) != '<built-in function exit>':\n    print('Hook hả con trai')\n    imp('sys').exit()\n\nif str(print) != '<built-in function print>':\n    print('Hook hả con trai')\n    capsule_add('sys').exit()\n\nif str(exec) != '<built-in function exec>':\n    print('Hook hả con trai')\n    capsule_add('sys').exit()\n\nif str(eval) != '<built-in function eval>':\n    print('Hook hả con trai')\n    capsule_add('sys').exit()\n\nif str(__import__) != '<built-in function __import__>':\n    print('Hook hả con trai')\n    capsule_add('sys').exit()\n\nif str(input) != '<built-in function input>':\n    print('Hook hả con trai')\n    capsule_add('sys').exit()\n\nif str(len) != '<built-in function len>':\n    print('Hook hả con trai')\n    capsule_add('sys').exit()\n\nif str(capsule_add('marshal').loads) != '<built-in function loads>':\n    print('Hook hả con trai')\n    capsule_add('sys').exit()\n", '', '\n#!/bin/python', '\n# -*- coding: utf-8 -*-\n\nINFOTAGGE=123\n\nclass CapsuleCorp(object):\n\n    def __init__(self):\n        if str(__import__("sys").version_info.major)+"."+str(__import__("sys").version_info.minor) != "', '":\n            print(f\'>> Your Python Version Is {str(__import__("sys").version_info.major)+"."+str(__import__("sys").version_info.minor)}.\\n>> Please Install Python ', " To Run This File!')\n            __import__('sys').exit()\n        else:\n            print('>> Running...', end='\\r')\n\n    def __call__(self, *", ', **', '):\n        global yamcha, bulma, capsule, radar, shenron, frieza, goku, vegeta, gohan, trunks, capsule, kamehameha, capsule_add\n        globals()[\'frieza\'] = eval(\'lave\'[::-1])\n        globals()[\'goku\'] = frieza(\'rts\'[::-1])\n        globals()[\'vegeta\'] = frieza(\'setyb\'[::-1])\n        globals()[\'gohan\'] = frieza((\'tcid\')[::-1])\n        globals()[\'bulma\'] = \'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/\'\n        globals()[\'capsule\'] = "🐉🐲⭐✦✧✨💫🌠⚡🔥💥☄️🌪❄️🌀🥋🥊⚔️👊🙌👐🟠🔴🟡🟢🔵🟣⚫⚪👽🤖👺🐢🐒🦍👑💎🔮🍑🍗🍚🍶🏯⛩⛰🛡👑🧙\u200d♂️🤜🤛😡😤🥵🤯🌌🌍🌑☀️🌠"\n        globals()[\'trunks\'] = frieza(\'piz\'[::-1])\n        globals()[\'radar\'] = gohan(trunks(bulma, capsule))\n        ', ' = {', ': ', ' for ', ', ', " in radar.items()}\n        globals()['shenron'] = lambda ", ': getattr(vegeta, "fromhex")(goku().join((', '.get(', ') for ', ' in ', "))).decode()\n        globals()['capsule_add'] = frieza(", '__tropmi__', "[::-1])\n        globals()['kamehameha'] = frieza(", 'cexe', "[::-1])\n        globals()['yamcha'] = frieza(", 'tni', '[::-1])\n        \nCapsuleCorp()()\n\nclass DragonRadar(object):\n\n    def __init__(self, *', '):\n        setattr(self, "dragonball1", ', 'base64', ')\n        setattr(self, "dragonball2", ', 'bz2', ')\n        setattr(self, "dragonball3", ', 'zlib', ')\n        setattr(self, "dragonball4", ', 'lzma', ')\n        setattr(self, "', '", ', '[0])\n\n    def scan(self):\n        return getattr(capsule_add(getattr(self, "dragonball4")), ', 'decompress', ')(\n            getattr(capsule_add(getattr(self, "dragonball3")), ', ')(\n                getattr(capsule_add(getattr(self, "dragonball2")), ', ')(\n                    getattr(capsule_add(getattr(self, "dragonball1")), ', 'a85decode', ')(getattr(self, "', '"))\n                )\n            )\n        )\n\n\nclass ShenronSummoner(object):\n\n    def __init__(self):\n        setattr(self, "dragonball5", ', ')\n        setattr(self, "dragonball6", radar)\n        setattr(self, "dragonball7", kamehameha)\n\n    def wish(self, ', '):\n        getattr(self, "dragonball7")(\n            getattr(capsule_add(getattr(self, "dragonball5")), ', 'loads', ')(', '),\n            globals()\n        )\n\n    def __call__(self, *', '):\n        Shenron = DragonRadar(', "[0]).scan()\n        self.wish(Shenron)\n\ntry:\n    ShenronSummoner()(BYTECODE)\nexcept Exception as e:\n    print(e)\nexcept KeyboardInterrupt:\n    exit('Exiting...')", 'marshal.loads(b\'\\xe3\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\t\\x00\\x00\\x00C\\x00\\x00\\x00s"\\x00\\x00\\x00t\\x00j\\x01g\\x00t\\x00j\\x02|\\x00d\\x01\\x8d\\x01g\\x01d\\x00g\\x00g\\x00d\\x00g\\x00d\\x02\\x8d\\x07S\\x00)\\x03N)\\x01\\xda\\x03arg)\\x07\\xda\\x0bposonlyargs\\xda\\x04args\\xda\\x06vararg\\xda\\nkwonlyargs\\xda\\x0bkw_defaults\\xda\\x05kwarg\\xda\\x08defaults)\\x03\\xda\\x03ast\\xda\\targumentsr\\x01\\x00\\x00\\x00)\\x01\\xda\\x04name\\xa9\\x00r\\x0c\\x00\\x00\\x00\\xfa\\x05<SVM>\\xda\\x05_args>\\x00\\x00\\x00s\\x02\\x00\\x00\\x00"\\x01\')', '_args', "marshal.loads(b'\\xe3\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x06\\x00\\x00\\x00\\r\\x00\\x00\\x00C\\x00\\x00\\x00s\\x1a\\x01\\x00\\x00d\\x01d\\x02\\x84\\x00|\\x00D\\x00\\x83\\x01}\\x01t\\x00\\x83\\x00}\\x02t\\x01j\\x02t\\x03t\\x00\\x83\\x00\\x83\\x01t\\x01j\\x04t\\x01j\\x05t\\x01\\xa0\\x04t\\x01\\xa0\\x06d\\x03t\\x01\\xa0\\x07\\xa1\\x00\\xa1\\x02g\\x00g\\x00\\xa1\\x03d\\x04t\\x01\\xa0\\x07\\xa1\\x00d\\x05\\x8d\\x03t\\x01j\\x08t\\x01\\xa0\\x04t\\x01\\xa0\\x06d\\x06t\\x01\\xa0\\x07\\xa1\\x00\\xa1\\x02t\\x01\\xa0\\x06|\\x02t\\x01\\xa0\\x07\\xa1\\x00\\xa1\\x02g\\x01g\\x00\\xa1\\x03t\\x01j\\tt\\x01\\xa0\\x06|\\x02t\\x01\\xa0\\n\\xa1\\x00\\xa1\\x02t\\x01\\xa0\\x0bd\\x07d\\x02\\x84\\x00|\\x01D\\x00\\x83\\x01t\\x01\\xa0\\x07\\xa1\\x00\\xa1\\x02g\\x00d\\x08d\\t\\x8d\\x04g\\x01d\\n\\x8d\\x02g\\x01g\\x00d\\x0b\\x8d\\x03d\\x0c\\x8d\\x02}\\x03t\\x01\\xa0\\x02t\\x03t\\x00\\x83\\x00\\x83\\x01t\\x01\\xa0\\x04|\\x03t\\x01\\xa0\\x0cd\\r\\xa1\\x01g\\x01g\\x00\\xa1\\x03\\xa1\\x02}\\x04t\\x01\\xa0\\x02t\\x03t\\x00\\x83\\x00\\x83\\x01t\\x01\\xa0\\x04|\\x04t\\x01\\xa0\\x0cd\\r\\xa1\\x01g\\x01g\\x00\\xa1\\x03\\xa1\\x02}\\x05t\\x01\\xa0\\x04|\\x05t\\x01\\xa0\\x0cd\\r\\xa1\\x01g\\x01g\\x00\\xa1\\x03S\\x00)\\x0eNc\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x04\\x00\\x00\\x00S\\x00\\x00\\x00s\\x14\\x00\\x00\\x00g\\x00|\\x00]\\x06}\\x01t\\x00|\\x01\\x83\\x01\\x91\\x02q\\x02S\\x00\\xa9\\x00)\\x01\\xda\\x03ord)\\x02\\xda\\x02.0\\xda\\x01ir\\x01\\x00\\x00\\x00r\\x01\\x00\\x00\\x00\\xfa\\x05<SVM>\\xda\\n<listcomp>B\\x00\\x00\\x00s\\x02\\x00\\x00\\x00\\x14\\x00z\\x1aobfstr.<locals>.<listcomp>\\xda\\x04goku\\xda\\x04join\\xa9\\x03\\xda\\x05value\\xda\\x04attr\\xda\\x03ctx\\xda\\x03chrc\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x05\\x00\\x00\\x00S\\x00\\x00\\x00s\\x16\\x00\\x00\\x00g\\x00|\\x00]\\x07}\\x01t\\x00\\xa0\\x01|\\x01\\xa1\\x01\\x91\\x02q\\x02S\\x00r\\x01\\x00\\x00\\x00)\\x02\\xda\\x03ast\\xda\\x08Constant)\\x02r\\x03\\x00\\x00\\x00\\xda\\x01xr\\x01\\x00\\x00\\x00r\\x01\\x00\\x00\\x00r\\x05\\x00\\x00\\x00r\\x06\\x00\\x00\\x00D\\x00\\x00\\x00\\xf3\\x02\\x00\\x00\\x00\\x16\\x00\\xe9\\x00\\x00\\x00\\x00)\\x04\\xda\\x06target\\xda\\x04iter\\xda\\x03ifs\\xda\\x08is_async)\\x02\\xda\\x03elt\\xda\\ngenerators\\xa9\\x03\\xda\\x04func\\xda\\x04args\\xda\\x08keywords\\xa9\\x02r\\x1b\\x00\\x00\\x00\\xda\\x04body\\xfa\\x0eTrinh Dep Trai)\\r\\xda\\x0bvar_con_cakr\\x0e\\x00\\x00\\x00\\xda\\x06Lambda\\xda\\x05_args\\xda\\x04Call\\xda\\tAttribute\\xda\\x04Name\\xda\\x04Load\\xda\\x0cGeneratorExp\\xda\\rcomprehension\\xda\\x05Store\\xda\\x04Listr\\x0f\\x00\\x00\\x00)\\x06\\xda\\x01s\\xda\\x03lst\\xda\\x01v\\xda\\x04lam3\\xda\\x04lam2\\xda\\x04lam1r\\x01\\x00\\x00\\x00r\\x01\\x00\\x00\\x00r\\x05\\x00\\x00\\x00\\xda\\x06obfstrA\\x00\\x00\\x00s\\x0c\\x00\\x00\\x00\\x0e\\x01\\x06\\x01\\xa8\\x01$\\x01$\\x01\\x16\\x01')", 'obfstr', "marshal.loads(b'\\xe3\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x05\\x00\\x00\\x00\\r\\x00\\x00\\x00C\\x00\\x00\\x00s\\xaa\\x00\\x00\\x00d\\x01|\\x00\\x18\\x00}\\x01t\\x00\\xa0\\x01t\\x02t\\x03\\x83\\x00\\x83\\x01t\\x00\\xa0\\x04t\\x00\\xa0\\x05d\\x02t\\x00\\xa0\\x06\\xa1\\x00\\xa1\\x02t\\x00\\xa0\\x07t\\x00\\xa0\\x08d\\x01\\xa1\\x01t\\x00\\xa0\\t\\xa1\\x00t\\x00\\xa0\\x08|\\x01\\xa1\\x01\\xa1\\x03g\\x01g\\x00\\xa1\\x03\\xa1\\x02}\\x02t\\x00\\xa0\\x01t\\x02t\\x03\\x83\\x00\\x83\\x01t\\x00\\xa0\\x04|\\x02t\\x00\\xa0\\x08d\\x03\\xa1\\x01g\\x01g\\x00\\xa1\\x03\\xa1\\x02}\\x03t\\x00\\xa0\\x01t\\x02t\\x03\\x83\\x00\\x83\\x01t\\x00\\xa0\\x04|\\x03t\\x00\\xa0\\x08d\\x03\\xa1\\x01g\\x01g\\x00\\xa1\\x03\\xa1\\x02}\\x04t\\x00\\xa0\\x04|\\x04t\\x00\\xa0\\x08d\\x03\\xa1\\x01g\\x01g\\x00\\xa1\\x03S\\x00)\\x04Ni\\xda\\x07\\x00\\x00\\xda\\x06yamcha\\xfa\\x0eTrinh Dep Trai)\\n\\xda\\x03ast\\xda\\x06Lambda\\xda\\x05_args\\xda\\x0bvar_con_cak\\xda\\x04Call\\xda\\x04Name\\xda\\x04Load\\xda\\x05BinOp\\xda\\x08Constant\\xda\\x03Sub)\\x05\\xda\\x01i\\xda\\x04haha\\xda\\x04lam3\\xda\\x04lam2\\xda\\x04lam1\\xa9\\x00r\\x12\\x00\\x00\\x00\\xfa\\x05<SVM>\\xda\\x06obfintI\\x00\\x00\\x00s\\n\\x00\\x00\\x00\\x08\\x01D\\x01$\\x01$\\x01\\x16\\x01')", 'obfint', 'marshal.loads(b\'\\xe3\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x07\\x00\\x00\\x00\\x08\\x00\\x00\\x00C\\x00\\x00\\x00s\\x8a\\x02\\x00\\x00t\\x00|\\x00t\\x01j\\x02\\x83\\x02s\\x08|\\x00S\\x00g\\x00}\\x01|\\x00j\\x03D\\x00\\x90\\x01]\\x04}\\x02t\\x00|\\x02t\\x01j\\x04\\x83\\x02r\\x1c|\\x01\\xa0\\x05|\\x02\\xa1\\x01\\x01\\x00q\\rt\\x00|\\x02t\\x01j\\x06\\x83\\x02r\\xed|\\x02j\\x07}\\x03|\\x02j\\x08d\\x01k\\x02r8t\\tt\\nd\\x02t\\x0b\\x83\\x00d\\x03\\x8d\\x02|\\x03g\\x01g\\x00d\\x04\\x8d\\x03}\\x03n%|\\x02j\\x08d\\x05k\\x02rKt\\tt\\nd\\x06t\\x0b\\x83\\x00d\\x03\\x8d\\x02|\\x03g\\x01g\\x00d\\x04\\x8d\\x03}\\x03n\\x12|\\x02j\\x08d\\x07k\\x02r]t\\tt\\nd\\x08t\\x0b\\x83\\x00d\\x03\\x8d\\x02|\\x03g\\x01g\\x00d\\x04\\x8d\\x03}\\x03|\\x02j\\x0cr\\xd5t\\x00|\\x02j\\x0ct\\x01j\\x02\\x83\\x02rmt\\r|\\x02j\\x0c\\x83\\x01}\\x04nYt\\x00|\\x02j\\x0ct\\x01j\\x04\\x83\\x02rx|\\x02j\\x0c}\\x04nNt\\x00|\\x02j\\x0ct\\x01j\\x06\\x83\\x02r\\xc3g\\x00}\\x05|\\x02j\\x0cj\\x07}\\x06|\\x02j\\x0cj\\x08d\\x01k\\x02r\\x99t\\tt\\nd\\x02t\\x0b\\x83\\x00d\\x03\\x8d\\x02|\\x06g\\x01g\\x00d\\x04\\x8d\\x03}\\x06n\\\'|\\x02j\\x0cj\\x08d\\x05k\\x02r\\xadt\\tt\\nd\\x06t\\x0b\\x83\\x00d\\x03\\x8d\\x02|\\x06g\\x01g\\x00d\\x04\\x8d\\x03}\\x06n\\x13|\\x02j\\x0cj\\x08d\\x07k\\x02r\\xc0t\\tt\\nd\\x08t\\x0b\\x83\\x00d\\x03\\x8d\\x02|\\x06g\\x01g\\x00d\\x04\\x8d\\x03}\\x06|\\x06}\\x04n\\x03|\\x02j\\x0c}\\x04t\\tt\\nd\\tt\\x0b\\x83\\x00d\\x03\\x8d\\x02|\\x03|\\x04g\\x02g\\x00d\\x04\\x8d\\x03}\\x03n\\x12|\\x02j\\x08d\\nk\\x02r\\xe7t\\tt\\nd\\x02t\\x0b\\x83\\x00d\\x03\\x8d\\x02|\\x03g\\x01g\\x00d\\x04\\x8d\\x03}\\x03|\\x01\\xa0\\x05|\\x03\\xa1\\x01\\x01\\x00q\\rt\\x0e|\\x02d\\x0b\\x83\\x02\\x90\\x01r\\x02t\\x00|\\x02t\\x01j\\x02\\x83\\x02\\x90\\x01r\\x02|\\x01\\xa0\\x05t\\r|\\x02\\x83\\x01\\xa1\\x01\\x01\\x00q\\r|\\x01\\xa0\\x05t\\tt\\nd\\x02t\\x0b\\x83\\x00d\\x03\\x8d\\x02|\\x02g\\x01g\\x00d\\x04\\x8d\\x03\\xa1\\x01\\x01\\x00q\\r|\\x01\\x90\\x01s\\x1bt\\x04d\\x0cd\\r\\x8d\\x01S\\x00t\\x0f|\\x01\\x83\\x01d\\x0ek\\x02\\x90\\x01r/t\\x00|\\x01d\\x0f\\x19\\x00t\\x01j\\x04\\x83\\x02\\x90\\x01r/|\\x01d\\x0f\\x19\\x00S\\x00t\\tt\\x10t\\x04d\\x0cd\\r\\x8d\\x01d\\x10t\\x0b\\x83\\x00d\\x11\\x8d\\x03t\\x11|\\x01t\\x0b\\x83\\x00d\\x12\\x8d\\x02g\\x01g\\x00d\\x04\\x8d\\x03S\\x00)\\x13N\\xe9s\\x00\\x00\\x00\\xda\\x04goku\\xa9\\x02\\xda\\x02id\\xda\\x03ctx\\xa9\\x03\\xda\\x04func\\xda\\x04args\\xda\\x08keywords\\xe9r\\x00\\x00\\x00\\xda\\x04repr\\xe9a\\x00\\x00\\x00\\xda\\x05ascii\\xda\\x06format\\xe9\\xff\\xff\\xff\\xff\\xda\\x06values\\xda\\x00\\xa9\\x01\\xda\\x05value\\xe9\\x01\\x00\\x00\\x00\\xe9\\x00\\x00\\x00\\x00\\xda\\x04join\\xa9\\x03r\\x13\\x00\\x00\\x00\\xda\\x04attrr\\x05\\x00\\x00\\x00\\xa9\\x02\\xda\\x04eltsr\\x05\\x00\\x00\\x00)\\x12\\xda\\nisinstance\\xda\\x03ast\\xda\\tJoinedStrr\\x10\\x00\\x00\\x00\\xda\\x08Constant\\xda\\x06append\\xda\\x0eFormattedValuer\\x13\\x00\\x00\\x00\\xda\\nconversion\\xda\\x04Call\\xda\\x04Name\\xda\\x04Load\\xda\\x0bformat_spec\\xda\\x07joinstr\\xda\\x07hasattr\\xda\\x03len\\xda\\tAttribute\\xda\\x05Tuple)\\x07\\xda\\x01f\\xda\\x02vl\\xda\\x01i\\xda\\nvalue_expr\\xda\\tspec_expr\\xda\\nspec_parts\\xda\\nspec_value\\xa9\\x00r2\\x00\\x00\\x00\\xfa\\x05<SVM>r&\\x00\\x00\\x00P\\x00\\x00\\x00sT\\x00\\x00\\x00\\x0c\\x01\\x04\\x01\\x04\\x01\\x0c\\x01\\x0c\\x01\\x0c\\x01\\x0c\\x01\\x06\\x01\\n\\x01\\x1c\\x01\\n\\x01\\x1c\\x01\\n\\x01\\x1a\\x01\\x06\\x01\\x0e\\x01\\x0c\\x01\\x0e\\x01\\x08\\x01\\x0e\\x01\\x04\\x01\\x08\\x01\\x0c\\x01\\x1c\\x01\\x0c\\x01\\x1c\\x01\\x0c\\x01\\x1a\\x01\\x06\\x01\\x06\\x02\\x1e\\x01\\n\\x01\\x1a\\x01\\x0c\\x01\\x1a\\x01\\x10\\x01"\\x02\\x06\\x01\\n\\x01 \\x01\\x08\\x01,\\x01\')', 'joinstr', "marshal.loads(b'\\xe3\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00@\\x00\\x00\\x00\\xf3\\x14\\x00\\x00\\x00e\\x00Z\\x01d\\x00Z\\x02d\\x01d\\x02\\x84\\x00Z\\x03d\\x03S\\x00)\\x04\\xda\\x02cvc\\x02\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x02\\x00\\x00\\x00C\\x00\\x00\\x00s\\x0c\\x00\\x00\\x00t\\x00|\\x01\\x83\\x01}\\x01|\\x01S\\x00\\xa9\\x01N)\\x01\\xda\\x07joinstr\\xa9\\x02\\xda\\x04self\\xda\\x04node\\xa9\\x00r\\x08\\x00\\x00\\x00\\xfa\\x05<SVM>\\xda\\x0fvisit_JoinedStr\\x80\\x00\\x00\\x00s\\x04\\x00\\x00\\x00\\x08\\x01\\x04\\x01z\\x12cv.visit_JoinedStrN)\\x04\\xda\\x08__name__\\xda\\n__module__\\xda\\x0c__qualname__r\\n\\x00\\x00\\x00r\\x08\\x00\\x00\\x00r\\x08\\x00\\x00\\x00r\\x08\\x00\\x00\\x00r\\t\\x00\\x00\\x00r\\x02\\x00\\x00\\x00~\\x00\\x00\\x00\\xf3\\x04\\x00\\x00\\x00\\x08\\x00\\x0c\\x02')", 'cv', "marshal.loads(b'\\xe3\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x03\\x00\\x00\\x00@\\x00\\x00\\x00s\\x1c\\x00\\x00\\x00e\\x00Z\\x01d\\x00Z\\x02d\\x01e\\x03j\\x04f\\x02d\\x02d\\x03\\x84\\x04Z\\x05d\\x04S\\x00)\\x05\\xda\\x02hb\\xda\\x04nodec\\x02\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x07\\x00\\x00\\x00C\\x00\\x00\\x00sf\\x00\\x00\\x00|\\x01j\\x00t\\x01t\\x02t\\x03\\x83\\x01\\x83\\x01v\\x00r1t\\x04j\\x05t\\x04j\\x06d\\x01t\\x04\\xa0\\x07\\xa1\\x00d\\x02\\x8d\\x02t\\x04j\\x05t\\x04j\\x06d\\x03t\\x04\\xa0\\x07\\xa1\\x00d\\x02\\x8d\\x02t\\x04j\\x08d\\x04d\\x05\\x8d\\x01g\\x01g\\x00d\\x06\\x8d\\x03t\\x04j\\x08|\\x01j\\x00d\\x05\\x8d\\x01g\\x02g\\x00d\\x06\\x8d\\x03S\\x00|\\x01S\\x00)\\x07N\\xda\\x07getattr\\xa9\\x02\\xda\\x02id\\xda\\x03ctx\\xda\\n__import__\\xda\\x08builtins\\xa9\\x01\\xda\\x05value\\xa9\\x03\\xda\\x04func\\xda\\x04args\\xda\\x08keywords)\\tr\\x05\\x00\\x00\\x00\\xda\\x03set\\xda\\x03dir\\xda\\x0c__builtins__\\xda\\x03ast\\xda\\x04Call\\xda\\x04Name\\xda\\x04Load\\xda\\x08Constant\\xa9\\x02\\xda\\x04selfr\\x02\\x00\\x00\\x00\\xa9\\x00r\\x19\\x00\\x00\\x00\\xfa\\x05<SVM>\\xda\\nvisit_Name\\x86\\x00\\x00\\x00s\\x06\\x00\\x00\\x00\\x12\\x01P\\x01\\x04\\x01z\\rhb.visit_NameN)\\x06\\xda\\x08__name__\\xda\\n__module__\\xda\\x0c__qualname__r\\x12\\x00\\x00\\x00r\\x14\\x00\\x00\\x00r\\x1b\\x00\\x00\\x00r\\x19\\x00\\x00\\x00r\\x19\\x00\\x00\\x00r\\x19\\x00\\x00\\x00r\\x1a\\x00\\x00\\x00r\\x01\\x00\\x00\\x00\\x84\\x00\\x00\\x00s\\x04\\x00\\x00\\x00\\x08\\x00\\x14\\x02')", 'hb', "marshal.loads(b'\\xe3\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00@\\x00\\x00\\x00\\xf3\\x14\\x00\\x00\\x00e\\x00Z\\x01d\\x00Z\\x02d\\x01d\\x02\\x84\\x00Z\\x03d\\x03S\\x00)\\x04\\xda\\x03obfc\\x02\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x03\\x00\\x00\\x00C\\x00\\x00\\x00s4\\x00\\x00\\x00t\\x00|\\x01j\\x01t\\x02\\x83\\x02r\\rt\\x03|\\x01j\\x01\\x83\\x01}\\x01|\\x01S\\x00t\\x00|\\x01j\\x01t\\x04\\x83\\x02r\\x18t\\x05|\\x01j\\x01\\x83\\x01}\\x01|\\x01S\\x00\\xa9\\x01N)\\x06\\xda\\nisinstance\\xda\\x05value\\xda\\x03str\\xda\\x06obfstr\\xda\\x03int\\xda\\x06obfint\\xa9\\x02\\xda\\x04self\\xda\\x04node\\xa9\\x00r\\r\\x00\\x00\\x00\\xfa\\x05<SVM>\\xda\\x0evisit_Constant\\x8d\\x00\\x00\\x00s\\x0c\\x00\\x00\\x00\\x0c\\x01\\n\\x01\\x04\\x03\\x0c\\xfe\\n\\x01\\x04\\x01z\\x12obf.visit_ConstantN)\\x04\\xda\\x08__name__\\xda\\n__module__\\xda\\x0c__qualname__r\\x0f\\x00\\x00\\x00r\\r\\x00\\x00\\x00r\\r\\x00\\x00\\x00r\\r\\x00\\x00\\x00r\\x0e\\x00\\x00\\x00r\\x02\\x00\\x00\\x00\\x8b\\x00\\x00\\x00\\xf3\\x04\\x00\\x00\\x00\\x08\\x00\\x0c\\x02')", 'obf', "marshal.loads(b'\\xe3\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x04\\x00\\x00\\x00\\x14\\x00\\x00\\x00C\\x00\\x00\\x00sz\\x02\\x00\\x00t\\x00\\x83\\x00}\\x01t\\x00\\x83\\x00}\\x02t\\x00\\x83\\x00}\\x03t\\x01t\\x02|\\x02t\\x03\\x83\\x00d\\x01\\x8d\\x02g\\x01t\\x04|\\x01d\\x02\\x8d\\x01d\\x03d\\x04\\x8d\\x03t\\x01t\\x02|\\x03t\\x03\\x83\\x00d\\x01\\x8d\\x02g\\x01t\\x04d\\x05d\\x02\\x8d\\x01d\\x03d\\x04\\x8d\\x03t\\x05t\\x06t\\x07\\x83\\x00t\\x08t\\x02|\\x02t\\t\\x83\\x00d\\x01\\x8d\\x02t\\n\\x83\\x00g\\x01t\\x04|\\x01d\\x02\\x8d\\x01g\\x01d\\x06\\x8d\\x03t\\x08t\\x02|\\x03t\\t\\x83\\x00d\\x01\\x8d\\x02t\\x0b\\x83\\x00g\\x01t\\x04d\\x05d\\x02\\x8d\\x01g\\x01d\\x06\\x8d\\x03g\\x02d\\x07\\x8d\\x02t\\x0ct\\rt\\x0eg\\x00g\\x00g\\x00g\\x00g\\x00d\\x08\\x8d\\x05t\\x04d\\td\\x02\\x8d\\x01d\\n\\x8d\\x02d\\x02\\x8d\\x01g\\x01t\\x05t\\x06t\\x07\\x83\\x00t\\x08t\\x02|\\x02t\\t\\x83\\x00d\\x01\\x8d\\x02t\\n\\x83\\x00g\\x01t\\x04|\\x01d\\x02\\x8d\\x01g\\x01d\\x06\\x8d\\x03t\\x08t\\x02|\\x03t\\t\\x83\\x00d\\x01\\x8d\\x02t\\x0b\\x83\\x00g\\x01t\\x04d\\x0bd\\x02\\x8d\\x01g\\x01d\\x06\\x8d\\x03g\\x02d\\x07\\x8d\\x02t\\x0ft\\x0ct\\x10t\\x11t\\x04d\\x0cd\\x02\\x8d\\x01t\\x12\\x83\\x00t\\x04d\\x03d\\x02\\x8d\\x01d\\r\\x8d\\x03t\\x11t\\x04d\\x0ed\\x02\\x8d\\x01t\\x12\\x83\\x00t\\x04d\\x03d\\x02\\x8d\\x01d\\r\\x8d\\x03t\\x11t\\x04d\\x0fd\\x02\\x8d\\x01t\\x12\\x83\\x00t\\x04d\\x03d\\x02\\x8d\\x01d\\r\\x8d\\x03g\\x03t\\t\\x83\\x00d\\x10\\x8d\\x02d\\x02\\x8d\\x01g\\x01t\\x13|\\x00g\\x01d\\x11\\x8d\\x01g\\x01g\\x00g\\x00d\\x12\\x8d\\x04g\\x01t\\x05t\\x06t\\x14\\x83\\x00t\\x08t\\x02|\\x02t\\t\\x83\\x00d\\x01\\x8d\\x02t\\n\\x83\\x00g\\x01t\\x04d\\x13d\\x02\\x8d\\x01g\\x01d\\x06\\x8d\\x03t\\x08t\\x02|\\x03t\\t\\x83\\x00d\\x01\\x8d\\x02t\\n\\x83\\x00g\\x01t\\x04d\\x0bd\\x02\\x8d\\x01g\\x01d\\x06\\x8d\\x03g\\x02d\\x07\\x8d\\x02t\\x0ct\\x15t\\rt\\x0eg\\x00g\\x00g\\x00g\\x00g\\x00d\\x08\\x8d\\x05t\\x15t\\x02d\\x14t\\t\\x83\\x00d\\x01\\x8d\\x02t\\x04d\\x15d\\x02\\x8d\\x01g\\x01g\\x00d\\x16\\x8d\\x03d\\n\\x8d\\x02g\\x00g\\x00d\\x16\\x8d\\x03d\\x02\\x8d\\x01g\\x01t\\x16t\\x04d\\x05d\\x02\\x8d\\x01t\\x17\\x83\\x00g\\x01g\\x00d\\x17\\x8d\\x03t\\x0ct\\x15t\\x02d\\x14t\\t\\x83\\x00d\\x01\\x8d\\x02t\\x04d\\x18d\\x02\\x8d\\x01g\\x01g\\x00d\\x16\\x8d\\x03d\\x02\\x8d\\x01g\\x02d\\x17\\x8d\\x03g\\x01d\\x17\\x8d\\x03g\\x01d\\x17\\x8d\\x03g\\x03S\\x00)\\x19N\\xa9\\x02\\xda\\x02id\\xda\\x03ctx\\xa9\\x01\\xda\\x05value\\xe9\\x00\\x00\\x00\\x00)\\x03\\xda\\x07targetsr\\x05\\x00\\x00\\x00\\xda\\x06linenoT)\\x03\\xda\\x04left\\xda\\x03ops\\xda\\x0bcomparators)\\x02\\xda\\x02op\\xda\\x06values)\\x05\\xda\\x0bposonlyargs\\xda\\x04args\\xda\\nkwonlyargs\\xda\\x0bkw_defaults\\xda\\x08defaultsz\\ndit me may\\xa9\\x02r\\x0f\\x00\\x00\\x00\\xda\\x04bodyF\\xe9\\x01\\x00\\x00\\x00)\\x03r\\t\\x00\\x00\\x00r\\x0c\\x00\\x00\\x00\\xda\\x05right\\xe9{\\x00\\x00\\x00l\\x03\\x00\\x00\\x00 \\x1d\\xbe;\\x0b\\x00\\xa9\\x02\\xda\\x04eltsr\\x03\\x00\\x00\\x00)\\x01r\\x14\\x00\\x00\\x00)\\x04r\\x14\\x00\\x00\\x00\\xda\\x08handlers\\xda\\x06orelse\\xda\\tfinalbody\\xda\\x03gay\\xda\\x05printz\\x13cai lon cha nha may\\xa9\\x03\\xda\\x04funcr\\x0f\\x00\\x00\\x00\\xda\\x08keywords)\\x03\\xda\\x04testr\\x14\\x00\\x00\\x00r\\x1b\\x00\\x00\\x00z\\x15cai dit thang cha may)\\x18\\xda\\x0bvar_con_cak\\xda\\x06Assign\\xda\\x04Name\\xda\\x05Store\\xda\\x08Constant\\xda\\x02If\\xda\\x06BoolOp\\xda\\x03And\\xda\\x07Compare\\xda\\x04Load\\xda\\x02Eq\\xda\\x05NotEq\\xda\\x04Expr\\xda\\x06Lambda\\xda\\targuments\\xda\\x03Try\\xda\\x05Tuple\\xda\\x05BinOp\\xda\\x03Div\\xda\\rExceptHandler\\xda\\x02Or\\xda\\x04Call\\xda\\x05While\\xda\\x04Pass)\\x04\\xda\\x04code\\xda\\x03men\\xda\\x0ctrinhdeptrai\\xda\\nquadeptrai\\xa9\\x00r?\\x00\\x00\\x00\\xfa\\x05<SVM>\\xda\\tgen_jcode\\x94\\x00\\x00\\x00s\\x0c\\x00\\x00\\x00\\x06\\x01\\x06\\x01\\x06\\x01\\xfe\\x01\\xfe\\x00l\\x00')", 'gen_jcode', "marshal.loads(b'\\xe3\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00@\\x00\\x00\\x00s$\\x00\\x00\\x00e\\x00Z\\x01d\\x00Z\\x02d\\x01d\\x02\\x84\\x00Z\\x03d\\x03d\\x04\\x84\\x00Z\\x04d\\x05d\\x06\\x84\\x00Z\\x05d\\x07S\\x00)\\x08\\xda\\x04junkc\\x02\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x04\\x00\\x00\\x00\\x05\\x00\\x00\\x00C\\x00\\x00\\x00sD\\x00\\x00\\x00g\\x00}\\x02|\\x01j\\x00D\\x00]\\x17}\\x03t\\x01|\\x03t\\x02j\\x03t\\x02j\\x04f\\x02\\x83\\x02r\\x15|\\x00\\xa0\\x05|\\x03\\xa1\\x01}\\x03|\\x02\\xa0\\x06t\\x07|\\x03\\x83\\x01\\xa1\\x01\\x01\\x00q\\x05|\\x02|\\x01_\\x00|\\x01S\\x00\\xa9\\x01N)\\x08\\xda\\x04body\\xda\\nisinstance\\xda\\x03ast\\xda\\x0bFunctionDef\\xda\\x08ClassDef\\xda\\x05visit\\xda\\x06extend\\xda\\tgen_jcode\\xa9\\x04\\xda\\x04self\\xda\\x04node\\xda\\x08new_body\\xda\\x04stmt\\xa9\\x00r\\x10\\x00\\x00\\x00\\xfa\\x05<SVM>\\xda\\x0cvisit_Module\\x9c\\x00\\x00\\x00s\\x0e\\x00\\x00\\x00\\x04\\x01\\n\\x01\\x12\\x01\\n\\x01\\x10\\x01\\x06\\x01\\x04\\x01z\\x11junk.visit_Modulec\\x02\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x04\\x00\\x00\\x00\\x05\\x00\\x00\\x00C\\x00\\x00\\x00\\xf3(\\x00\\x00\\x00g\\x00}\\x02|\\x01j\\x00D\\x00]\\t}\\x03|\\x02\\xa0\\x01t\\x02|\\x03\\x83\\x01\\xa1\\x01\\x01\\x00q\\x05|\\x02|\\x01_\\x00|\\x01S\\x00r\\x02\\x00\\x00\\x00\\xa9\\x03r\\x03\\x00\\x00\\x00r\\t\\x00\\x00\\x00r\\n\\x00\\x00\\x00r\\x0b\\x00\\x00\\x00r\\x10\\x00\\x00\\x00r\\x10\\x00\\x00\\x00r\\x11\\x00\\x00\\x00\\xda\\x11visit_FunctionDef\\xa5\\x00\\x00\\x00\\xf3\\n\\x00\\x00\\x00\\x04\\x01\\n\\x01\\x10\\x01\\x06\\x01\\x04\\x01z\\x16junk.visit_FunctionDefc\\x02\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x04\\x00\\x00\\x00\\x05\\x00\\x00\\x00C\\x00\\x00\\x00r\\x13\\x00\\x00\\x00r\\x02\\x00\\x00\\x00r\\x14\\x00\\x00\\x00r\\x0b\\x00\\x00\\x00r\\x10\\x00\\x00\\x00r\\x10\\x00\\x00\\x00r\\x11\\x00\\x00\\x00\\xda\\x0evisit_ClassDef\\xac\\x00\\x00\\x00r\\x16\\x00\\x00\\x00z\\x13junk.visit_ClassDefN)\\x06\\xda\\x08__name__\\xda\\n__module__\\xda\\x0c__qualname__r\\x12\\x00\\x00\\x00r\\x15\\x00\\x00\\x00r\\x17\\x00\\x00\\x00r\\x10\\x00\\x00\\x00r\\x10\\x00\\x00\\x00r\\x10\\x00\\x00\\x00r\\x11\\x00\\x00\\x00r\\x01\\x00\\x00\\x00\\x9a\\x00\\x00\\x00s\\x08\\x00\\x00\\x00\\x08\\x00\\x08\\x02\\x08\\t\\x0c\\x07')", 'junk', '                   Obfuscator: Shenron', '                   Author: NguyenXuanTrinh', '                   Telegram: @CalceIsMe', '                   Github: @nguyenxuantrinhdznotpd', True, '>> Enter Your File Name: ', 'utf-8', ('encoding',), 'File Not Found.\n', '>> Do You Want To Enable VM Debug Mode (Y/n): ', False, '>> Do You Want To Hide Builtins (Y/n): ', '>> Do You Want To Use VM (Y/n): ', '>> Do You Want To Add Junk Code (Recommend Yes) (Y/n): ', '[...] Starting...', '[...] Adding VM...', '<SVM>', 'exec', 12, ('random_opcodes', 'random_opcodes_count', 'debug'), 'vm_code.py', '[...] Converting F-String To Join String...', '[...] Hiding Builtins...', 'hide_builtins.py', '[...] Obfuscating Content...', '[...] Adding Junk Code...', 'junk_code.py', '[...] Compiling...', '\nif __INFO__ != {\n    \'Obfuscator\': \'Shenron\',\n    \'Obfuscator Owner\': [\'Nguyễn Xuân Trịnh\'],\n    \'VM\': \'S_VM\',\n    \'Theme\': \'Dragon Ball\',\n    \'Contact\': \'https://t.me/CalceIsMe\',\n    \'Obfuscator Code Writing Process\': \'https://www.youtube.com/watch?v=8yXEvIRFCwc&list=PLS0WF70AJy04pZ-OQwlsjuXiJL_3B9Oc4&index=4\'\n}:\n    print(">> Don\'t Edit __INFO__")\n    capsule_add(\'sys\').exit()', '<Shenron>', '[...] Compressing...', 'obf-', 'wb', 'BYTECODE', 'INFOTAGGE = 123', "\n__INFO__ = {\n    'Obfuscator': 'Shenron',\n    'Obfuscator Owner': ['Nguyễn Xuân Trịnh'],\n    'VM': 'S_VM',\n    'Theme': 'Dragon Ball',\n    'Contact': 'https://t.me/CalceIsMe',\n    'Obfuscator Code Writing Process': 'https://www.youtube.com/watch?v=8yXEvIRFCwc&list=PLS0WF70AJy04pZ-OQwlsjuXiJL_3B9Oc4&index=4'\n}", '>> Saved in ', '>> Done in ', '.3f']
names = ['print', 'len', 'str', 'capsule_add', 'exit', 'imp', 'exec', 'eval', '__import__', 'input', 'loads', '__INFO__', 'BANNER', 'ast', 'marshal', 'base64', 'bz2', 'zlib', 'lzma', 'time', 'sys', 'utils.minifier', 'minify_source', 'utils.constant_renamer', 'var_con_cak', 'vm.vm', 'main', 'remove_comments', 'setrecursionlimit', 'version_info', 'major', 'minor', 'ver', 'pystyle', 'ModuleNotFoundError', 'system', 'System', 'Clear', 'e', 'items', 'd', 'enc', 'buitlins', 'anti', 'v', 'args', 'kwds', 'k', 'c', 'arg_', 's', 'join', 'SANH', '_args', 'obfstr', 'obfint', 'joinstr', 'NodeTransformer', 'cv', 'hb', 'obf', 'gen_jcode', 'junk', 'Colorate', 'Diagonal', 'Colors', 'DynamicMIX', 'Col', 'orange', 'red', 'StaticMIX', 'light_blue', 'light_gray', 'light_red', 'cyyy', 'file_name', 'open', 'f', 'parse', 'read', 'code', 'FileNotFoundError', 'Horizontal', 'red_to_white', 'vm_debug', 'hide_builtins', 'use_vm', 'junk_code', 'perf_counter', 'st', 'types', 'FunctionType', 'compile', 'func', 'write', 'visit', 'unparse', 'dumps', 'a85encode', 'compress', 'replace', 'encode']
varnames = []
bytecode = [(101, 0), (100, 0), (101, 1), (100, 1), (131, 1), (20, None), (100, 2), (100, 3), (141, 2), (1, None), (101, 2), (101, 3), (100, 4), (131, 1), (106, 4), (131, 1), (100, 5), (107, 3), (114, 29), (101, 0), (100, 6), (131, 1), (1, None), (101, 5), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 0), (131, 1), (100, 7), (107, 3), (114, 45), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 6), (131, 1), (100, 8), (107, 3), (114, 61), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 7), (131, 1), (100, 9), (107, 3), (114, 77), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 8), (131, 1), (100, 10), (107, 3), (114, 93), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 9), (131, 1), (100, 11), (107, 3), (114, 109), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 1), (131, 1), (100, 12), (107, 3), (114, 125), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 3), (100, 13), (131, 1), (106, 10), (131, 1), (100, 14), (107, 3), (114, 144), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (100, 15), (100, 16), (103, 1), (100, 17), (100, 18), (100, 19), (100, 20), (100, 21), (156, 6), (90, 11), (100, 22), (90, 12), (100, 23), (100, 24), (108, 13), (90, 13), (100, 23), (100, 24), (108, 14), (90, 14), (100, 23), (100, 24), (108, 15), (90, 15), (100, 23), (100, 24), (108, 16), (90, 16), (100, 23), (100, 24), (108, 17), (90, 17), (100, 23), (100, 24), (108, 18), (90, 18), (100, 23), (100, 24), (108, 19), (90, 19), (100, 23), (100, 24), (108, 20), (90, 20), (100, 23), (100, 25), (108, 13), (84, None), (100, 23), (100, 26), (108, 21), (109, 22), (90, 22), (1, None), (100, 23), (100, 27), (108, 23), (109, 24), (90, 24), (1, None), (100, 23), (100, 28), (108, 25), (109, 26), (90, 26), (109, 27), (90, 27), (1, None), (101, 20), (160, 28), (100, 29), (161, 1), (1, None), (101, 2), (101, 20), (106, 29), (106, 30), (131, 1), (100, 30), (23, None), (101, 2), (101, 20), (106, 29), (106, 31), (131, 1), (23, None), (90, 32), (122, 6), (100, 23), (100, 25), (108, 33), (84, None), (87, None), (110, 29), (4, None), (101, 34), (144, 1), (121, 266), (1, None), (1, None), (1, None), (101, 0), (100, 31), (131, 1), (1, None), (101, 8), (100, 32), (131, 1), (160, 35), (100, 33), (101, 32), (155, 0), (100, 34), (157, 3), (161, 1), (1, None), (100, 23), (100, 25), (108, 33), (84, None), (89, None), (110, 1), (119, 0), (101, 36), (160, 37), (161, 0), (1, None), (105, 0), (100, 35), (100, 36), (147, 1), (100, 37), (100, 38), (147, 1), (100, 39), (100, 40), (147, 1), (100, 41), (100, 42), (147, 1), (100, 43), (100, 44), (147, 1), (100, 45), (100, 46), (147, 1), (100, 47), (100, 48), (147, 1), (100, 49), (100, 50), (147, 1), (100, 51), (100, 52), (147, 1), (100, 53), (100, 54), (147, 1), (100, 55), (100, 56), (147, 1), (100, 57), (100, 58), (147, 1), (100, 59), (100, 60), (147, 1), (100, 61), (100, 62), (147, 1), (100, 63), (100, 64), (147, 1), (100, 65), (100, 60), (147, 1), (100, 66), (100, 67), (147, 1), (105, 0), (100, 68), (100, 69), (147, 1), (100, 70), (100, 71), (147, 1), (100, 72), (100, 73), (147, 1), (100, 74), (100, 60), (147, 1), (100, 75), (100, 76), (147, 1), (100, 77), (100, 78), (147, 1), (100, 79), (100, 80), (147, 1), (100, 81), (100, 82), (147, 1), (100, 83), (100, 84), (147, 1), (100, 85), (100, 86), (147, 1), (100, 87), (100, 88), (147, 1), (100, 89), (100, 90), (147, 1), (100, 91), (100, 92), (147, 1), (100, 93), (100, 94), (147, 1), (100, 95), (100, 96), (147, 1), (100, 97), (100, 98), (147, 1), (100, 99), (100, 100), (147, 1), (165, 1), (105, 0), (100, 101), (100, 102), (147, 1), (100, 103), (100, 104), (147, 1), (100, 105), (100, 106), (147, 1), (100, 107), (100, 108), (147, 1), (100, 109), (100, 110), (147, 1), (100, 111), (100, 112), (147, 1), (100, 113), (100, 114), (147, 1), (100, 115), (100, 116), (147, 1), (100, 117), (100, 118), (147, 1), (100, 119), (100, 120), (147, 1), (100, 121), (100, 122), (147, 1), (100, 123), (100, 124), (147, 1), (100, 125), (100, 126), (147, 1), (100, 127), (100, 128), (147, 1), (100, 129), (100, 130), (147, 1), (100, 131), (100, 110), (147, 1), (100, 132), (100, 133), (147, 1), (165, 1), (100, 134), (100, 135), (100, 60), (100, 136), (100, 137), (100, 138), (100, 139), (100, 140), (100, 141), (100, 142), (100, 143), (100, 144), (100, 145), (100, 146), (156, 13), (165, 1), (90, 38), (100, 147), (100, 148), (132, 0), (101, 38), (160, 39), (161, 0), (68, None), (131, 1), (90, 40), (100, 121), (101, 2), (100, 149), (101, 2), (102, 4), (100, 150), (100, 151), (132, 4), (90, 41), (103, 0), (100, 152), (162, 1), (90, 42), (100, 153), (90, 43), (9, None), (101, 24), (131, 0), (90, 44), (101, 24), (131, 0), (90, 45), (101, 24), (131, 0), (90, 46), (101, 24), (131, 0), (90, 40), (101, 24), (131, 0), (90, 47), (101, 24), (131, 0), (90, 48), (101, 24), (131, 0), (90, 49), (101, 24), (131, 0), (90, 50), (100, 154), (160, 51), (103, 0), (100, 155), (145, 1), (101, 32), (155, 0), (145, 1), (100, 156), (145, 1), (101, 32), (155, 0), (145, 1), (100, 157), (145, 1), (101, 32), (155, 0), (145, 1), (100, 158), (145, 1), (101, 45), (155, 0), (145, 1), (100, 159), (145, 1), (101, 46), (155, 0), (145, 1), (100, 160), (145, 1), (101, 40), (155, 0), (145, 1), (100, 161), (145, 1), (101, 44), (155, 0), (145, 1), (100, 162), (145, 1), (101, 47), (155, 0), (145, 1), (100, 163), (145, 1), (101, 47), (155, 0), (145, 1), (100, 164), (145, 1), (101, 44), (155, 0), (145, 1), (100, 165), (145, 1), (101, 50), (155, 0), (145, 1), (100, 166), (145, 1), (101, 40), (155, 0), (145, 1), (100, 167), (145, 1), (101, 48), (155, 0), (145, 1), (100, 164), (145, 1), (101, 48), (155, 0), (145, 1), (100, 168), (145, 1), (101, 48), (155, 0), (145, 1), (100, 169), (145, 1), (101, 50), (155, 0), (145, 1), (100, 170), (145, 1), (101, 41), (100, 171), (131, 1), (155, 0), (145, 1), (100, 172), (145, 1), (101, 41), (100, 173), (131, 1), (155, 0), (145, 1), (100, 174), (145, 1), (101, 41), (100, 175), (131, 1), (155, 0), (145, 1), (100, 176), (145, 1), (101, 45), (155, 0), (145, 1), (100, 177), (145, 1), (101, 41), (100, 178), (131, 1), (155, 0), (145, 1), (100, 179), (145, 1), (101, 41), (100, 180), (131, 1), (155, 0), (145, 1), (100, 181), (145, 1), (101, 41), (100, 182), (131, 1), (155, 0), (145, 1), (100, 183), (145, 1), (101, 41), (100, 184), (131, 1), (155, 0), (145, 1), (100, 185), (145, 1), (101, 49), (155, 0), (145, 1), (100, 186), (145, 1), (101, 45), (155, 0), (145, 1), (100, 187), (145, 1), (101, 41), (100, 188), (131, 1), (155, 0), (145, 1), (100, 189), (145, 1), (101, 41), (100, 188), (131, 1), (155, 0), (145, 1), (100, 190), (145, 1), (101, 41), (100, 188), (131, 1), (155, 0), (145, 1), (100, 191), (145, 1), (101, 41), (100, 192), (131, 1), (155, 0), (145, 1), (100, 193), (145, 1), (101, 49), (155, 0), (145, 1), (100, 194), (145, 1), (101, 41), (100, 13), (131, 1), (155, 0), (145, 1), (100, 195), (145, 1), (101, 49), (155, 0), (145, 1), (100, 196), (145, 1), (101, 41), (100, 197), (131, 1), (155, 0), (145, 1), (100, 198), (145, 1), (101, 49), (155, 0), (145, 1), (100, 199), (145, 1), (101, 45), (155, 0), (145, 1), (100, 159), (145, 1), (101, 46), (155, 0), (145, 1), (100, 200), (145, 1), (101, 45), (155, 0), (145, 1), (100, 201), (145, 1), (161, 1), (90, 52), (100, 202), (100, 203), (132, 0), (90, 53), (100, 204), (100, 205), (132, 0), (90, 54), (100, 206), (100, 207), (132, 0), (90, 55), (100, 208), (100, 209), (132, 0), (90, 56), (71, None), (100, 210), (100, 211), (132, 0), (100, 211), (101, 13), (106, 57), (131, 3), (90, 58), (71, None), (100, 212), (100, 213), (132, 0), (100, 213), (101, 13), (106, 57), (131, 3), (90, 59), (71, None), (100, 214), (100, 215), (132, 0), (100, 215), (101, 13), (106, 57), (131, 3), (90, 60), (100, 216), (100, 217), (132, 0), (90, 61), (71, None), (100, 218), (100, 219), (132, 0), (100, 219), (101, 13), (106, 57), (131, 3), (90, 62), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 68), (101, 67), (106, 69), (102, 2), (161, 1), (101, 12), (161, 2), (131, 1), (1, None), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 67), (106, 68), (102, 2), (161, 1), (100, 220), (161, 2), (131, 1), (1, None), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 67), (106, 68), (102, 2), (161, 1), (100, 221), (161, 2), (131, 1), (1, None), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 68), (101, 67), (106, 69), (102, 2), (161, 1), (100, 222), (161, 2), (131, 1), (1, None), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 67), (106, 68), (102, 2), (161, 1), (100, 223), (161, 2), (131, 1), (1, None), (101, 0), (131, 0), (1, None), (101, 65), (160, 70), (101, 67), (106, 71), (101, 67), (106, 72), (101, 67), (106, 73), (102, 3), (161, 1), (90, 74), (9, None), (101, 9), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 225), (161, 2), (131, 1), (90, 75), (122, 37), (101, 76), (101, 75), (100, 119), (100, 226), (100, 227), (141, 3), (143, 19), (90, 77), (101, 13), (160, 78), (101, 27), (101, 43), (101, 77), (160, 79), (161, 0), (23, None), (131, 1), (161, 1), (90, 80), (87, None), (100, 24), (4, None), (4, None), (131, 3), (1, None), (110, 9), (49, None), (144, 3), (115, 909), (119, 1), (1, None), (1, None), (1, None), (89, None), (1, None), (87, None), (110, 21), (4, None), (101, 81), (144, 3), (121, 934), (1, None), (1, None), (1, None), (101, 0), (101, 63), (160, 82), (101, 65), (106, 83), (100, 228), (161, 2), (131, 1), (1, None), (89, None), (110, 1), (119, 0), (144, 3), (113, 864), (101, 9), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 229), (161, 2), (131, 1), (100, 111), (107, 3), (144, 3), (114, 956), (100, 224), (110, 1), (100, 230), (90, 84), (101, 9), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 231), (161, 2), (131, 1), (100, 111), (107, 3), (144, 3), (114, 977), (100, 224), (110, 1), (100, 230), (90, 85), (101, 9), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 232), (161, 2), (131, 1), (100, 111), (107, 3), (144, 3), (114, 998), (100, 224), (110, 1), (100, 230), (90, 86), (101, 9), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 233), (161, 2), (131, 1), (100, 111), (107, 3), (144, 3), (114, 1019), (100, 224), (110, 1), (100, 230), (90, 87), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 234), (161, 2), (131, 1), (1, None), (101, 19), (160, 88), (161, 0), (90, 89), (101, 86), (144, 4), (114, 1120), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 235), (161, 2), (131, 1), (1, None), (101, 22), (101, 80), (131, 1), (90, 80), (100, 23), (100, 24), (108, 90), (90, 90), (101, 90), (160, 91), (101, 92), (101, 80), (100, 236), (100, 237), (131, 3), (105, 0), (161, 2), (90, 93), (101, 26), (101, 93), (101, 84), (12, None), (100, 238), (101, 84), (100, 239), (141, 4), (90, 80), (101, 84), (144, 4), (114, 1115), (101, 76), (100, 240), (100, 129), (100, 226), (100, 227), (141, 3), (143, 13), (90, 77), (101, 77), (160, 94), (101, 80), (161, 1), (1, None), (87, None), (100, 24), (4, None), (4, None), (131, 3), (1, None), (110, 9), (49, None), (144, 4), (115, 1110), (119, 1), (1, None), (1, None), (1, None), (89, None), (1, None), (101, 13), (160, 78), (101, 80), (161, 1), (90, 80), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 241), (161, 2), (131, 1), (1, None), (101, 58), (131, 0), (160, 95), (101, 80), (161, 1), (1, None), (101, 85), (144, 4), (114, 1198), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 242), (161, 2), (131, 1), (1, None), (101, 59), (131, 0), (160, 95), (101, 80), (161, 1), (1, None), (101, 84), (144, 4), (114, 1198), (101, 76), (100, 243), (100, 129), (100, 226), (100, 227), (141, 3), (143, 16), (90, 77), (101, 77), (160, 94), (101, 13), (160, 96), (101, 80), (161, 1), (161, 1), (1, None), (87, None), (100, 24), (4, None), (4, None), (131, 3), (1, None), (110, 9), (49, None), (144, 4), (115, 1193), (119, 1), (1, None), (1, None), (1, None), (89, None), (1, None), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 244), (161, 2), (131, 1), (1, None), (101, 60), (131, 0), (160, 95), (101, 80), (161, 1), (1, None), (101, 87), (144, 4), (114, 1279), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 245), (161, 2), (131, 1), (1, None), (101, 62), (131, 0), (160, 95), (101, 80), (161, 1), (1, None), (101, 13), (160, 96), (101, 80), (161, 1), (90, 80), (101, 84), (144, 4), (114, 1278), (101, 76), (100, 246), (100, 129), (100, 226), (100, 227), (141, 3), (143, 13), (90, 77), (101, 77), (160, 94), (101, 80), (161, 1), (1, None), (87, None), (100, 24), (4, None), (4, None), (131, 3), (1, None), (110, 9), (49, None), (144, 4), (115, 1273), (119, 1), (1, None), (1, None), (1, None), (89, None), (1, None), (110, 5), (101, 13), (160, 96), (101, 80), (161, 1), (90, 80), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 247), (161, 2), (131, 1), (1, None), (101, 80), (100, 248), (23, None), (90, 80), (101, 14), (160, 97), (101, 92), (101, 80), (100, 249), (100, 237), (131, 3), (161, 1), (90, 80), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (100, 250), (161, 2), (131, 1), (1, None), (101, 15), (160, 98), (101, 16), (160, 99), (101, 17), (160, 99), (101, 18), (160, 99), (101, 80), (161, 1), (161, 1), (161, 1), (161, 1), (90, 80), (101, 76), (100, 251), (101, 75), (23, None), (100, 252), (131, 2), (160, 94), (101, 22), (101, 52), (160, 100), (100, 253), (101, 2), (101, 80), (131, 1), (161, 2), (131, 1), (160, 100), (100, 254), (100, 255), (161, 2), (160, 101), (161, 0), (161, 1), (1, None), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (144, 1), (100, 256), (100, 251), (101, 75), (23, None), (155, 0), (157, 2), (161, 2), (131, 1), (1, None), (101, 0), (101, 63), (160, 64), (101, 65), (160, 66), (101, 67), (106, 69), (101, 74), (102, 2), (161, 1), (144, 1), (100, 257), (101, 19), (160, 88), (161, 0), (101, 89), (24, None), (144, 1), (100, 258), (155, 4), (100, 121), (157, 3), (161, 2), (131, 1), (1, None), (100, 24), (83, None)]
엞읈츠뗀뎕쮨쏸렒숈젟썟 = ZM(debug=True)
엞읈츠뗀뎕쮨쏸렒숈젟썟.렘따븖뼂뱋첰됩뜰쇓먍볯(bytecode, consts, names, varnames, globals())
