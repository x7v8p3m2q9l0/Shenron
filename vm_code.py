
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

    def 얌묋쵕딘틣툧먉벤닰댕뉖(self, bytecode, consts, names, varnames, globals_):
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
            if opcode == 141:
                    keys = self.pop()  # tuple of keyword names
                    argc = oparg
                    args = [self.pop() for _ in range(argc)][::-1]
                    func = self.pop()
                    # last len(keys) args are keyword values
                    kw = {keys[i]: args[-len(keys)+i] for i in range(len(keys))}
                    posargs = args[:-len(keys)] if keys else args
                    result = func(*posargs, **kw)
                    self.push(result)

            elif opcode == 114:
                    val = self.pop()
                    if not val:
                        self.pc = oparg 
            elif opcode == 100: self.push(consts[oparg]) 
            elif opcode == 160:
                    if isinstance(names, (list, tuple)):
                        name = names[oparg]
                    elif isinstance(names, dict):
                        name = oparg
                    else:
                        raise VMError("LOAD_METHOD: unexpected names format")

                    obj = self.pop()


                    self.push((obj, name))

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

            elif opcode == 83: return self.pop() 
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

                        args = [a.encode() if isinstance(a, str) else a for a in args]
                        result = method(*args)
                    except AttributeError:
                        args = [a if isinstance(a, str) else a for a in args]
                        result = method(*args)
                    except Exception as e:
                        print(e)
                        result=None
                    self.push(result)

            elif opcode == 131:
                    argc = oparg
                    args = [self.pop() for _ in range(argc)][::-1]
                    func = self.pop()
                    result = func(*args)
                    self.push(result)

            elif opcode == 1: self.pop() 
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

            elif opcode == 20:
                    b = self.pop(); a = self.pop(); self.push(a * b)

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


            else:
                raise VMError(f"Unimplemented opcode {opcode}")

        return None

consts = [' ', '>> Running...', '\r', ('end',), 'sys', '<built-in function exit>', 'Hook hả con trai', '<built-in function print>', '<built-in function exec>', '<built-in function eval>', '<built-in function __import__>', '<built-in function input>', '<built-in function len>', 'marshal', '<built-in function loads>', 'hi', None]
names = ['print', 'len', 'str', 'capsule_add', 'exit', 'imp', 'exec', 'eval', '__import__', 'input', 'loads']
varnames = []
bytecode = [(101, 0), (100, 0), (101, 1), (100, 1), (131, 1), (20, None), (100, 2), (100, 3), (141, 2), (1, None), (101, 2), (101, 3), (100, 4), (131, 1), (106, 4), (131, 1), (100, 5), (107, 3), (114, 29), (101, 0), (100, 6), (131, 1), (1, None), (101, 5), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 0), (131, 1), (100, 7), (107, 3), (114, 45), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 6), (131, 1), (100, 8), (107, 3), (114, 61), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 7), (131, 1), (100, 9), (107, 3), (114, 77), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 8), (131, 1), (100, 10), (107, 3), (114, 93), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 9), (131, 1), (100, 11), (107, 3), (114, 109), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 1), (131, 1), (100, 12), (107, 3), (114, 125), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 2), (101, 3), (100, 13), (131, 1), (106, 10), (131, 1), (100, 14), (107, 3), (114, 144), (101, 0), (100, 6), (131, 1), (1, None), (101, 3), (100, 4), (131, 1), (160, 4), (161, 0), (1, None), (101, 0), (100, 15), (131, 1), (1, None), (100, 16), (83, None)]
툭턄뉑컧꺰톀뷱댒퀹똂읆 = ZM(debug=True)
툭턄뉑컧꺰톀뷱댒퀹똂읆.얌묋쵕딘틣툧먉벤닰댕뉖(bytecode, consts, names, varnames, globals())
