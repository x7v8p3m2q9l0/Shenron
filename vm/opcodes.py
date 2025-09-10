import dis

OP_HANDLERS = {
    dis.opmap[
        "LOAD_CONST"
    ]: """
                    value = consts[oparg]
                    self.push(value)
        """,        
    dis.opmap[
        "RETURN_VALUE"
    ]: """
                    return self.pop()
        """,
    dis.opmap[
        "BINARY_POWER"
    ]: """
                    b = self.pop(); a = self.pop(); self.push(a ** b)
        """,
    dis.opmap[
        "BINARY_MULTIPLY"
    ]: """
                    b = self.pop(); a = self.pop(); self.push(a * b)
        """,
    dis.opmap[
        "BINARY_MODULO"
    ]: """
                    b = self.pop(); a = self.pop(); self.push(a % b)
        """,
    dis.opmap[
        "BINARY_ADD"
    ]: """
                    b = self.pop(); a = self.pop(); self.push(a + b)
        """,
    dis.opmap[
        "BINARY_SUBTRACT"
    ]: """
                    b = self.pop(); a = self.pop(); self.push(a - b)
        """,
    dis.opmap[
        "BINARY_SUBSCR"
    ]: """
                    key = self.pop(); obj = self.pop(); self.push(obj[key])
        """,
    dis.opmap[
        "BINARY_FLOOR_DIVIDE"
    ]: """
                    b = self.pop(); a = self.pop(); self.push(a // b)
        """,
    dis.opmap[
        "BINARY_TRUE_DIVIDE"
    ]: """
                    b = self.pop(); a = self.pop(); self.push(a / b)
        """,
    dis.opmap[
        "INPLACE_FLOOR_DIVIDE"
    ]: """
                    b = self.pop(); a = self.pop(); self.push(a // b)
        """,
    dis.opmap[
        "INPLACE_TRUE_DIVIDE"
    ]: """
                    b = self.pop(); a = self.pop(); self.push(a / b)
        """,
    dis.opmap[
        "GET_LEN"
    ]: """
                    a = self.pop(); self.push(len(a))
        """,
    dis.opmap["POP_TOP"]: """ self.pop() """,
    dis.opmap["LOAD_CONST"]: """ self.push(consts[oparg]) """,
    # STORE_FAST
    dis.opmap[
        "STORE_FAST"
    ]: """
                    if not hasattr(self, "locals"):
                        self.locals = {}
                    varname = varnames[oparg] if isinstance(varnames, (list, tuple)) else str(oparg)
                    value = self.pop()
                    self.locals[varname] = value
        """,
    # LOAD_FAST
    dis.opmap[
        "LOAD_FAST"
    ]: """
                    if not hasattr(self, "locals"):
                        self.locals = {}
                    varname = varnames[oparg] if isinstance(varnames, (list, tuple)) else str(oparg)
                    if varname not in self.locals:
                        raise UnboundLocalError(f"local variable {varname!r} referenced before assignment")
                    self.push(self.locals[varname])
        """,
    dis.opmap["RETURN_VALUE"]: """ return self.pop() """,
    dis.opmap[
        "COMPARE_OP"
    ]: """
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
    dis.opmap[
        "POP_JUMP_IF_FALSE"
    ]: """
                    val = self.pop()
                    if not val:
                        self.pc = oparg """,
    dis.opmap[
        "POP_JUMP_IF_TRUE"
    ]: """
                    val = self.pop()
                    if val: 
                        self.pc = oparg
        """,
    dis.opmap[
        "LOAD_NAME"
    ]: """
                    import builtins

                    # get the identifier string from co_names
                    if isinstance(names, (list, tuple)):
                        name = names[oparg]
                    elif isinstance(names, dict):  # unlikely, but fallback
                        name = oparg
                    else:
                        raise VMError("LOAD_NAME: unexpected names format")

                    # runtime lookup order: locals → globals → builtins
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
        """,
    dis.opmap[
        "STORE_NAME"
    ]: """
                    # STORE_NAME stores into globals, not into the names array
                    if isinstance(names, (list, tuple)):
                        key = names[oparg]
                    else:
                        key = str(oparg)

                    value = self.pop()
                    self.globals[key] = value
        """,
    dis.opmap[
        "LOAD_GLOBAL"
    ]: """
                    if isinstance(names, (list, tuple)):
                        key = names[oparg]
                    else:
                        key = oparg
                    if key in globals_:
                        self.push(globals_[key])
                    else:
                        raise VMError(f"LOAD_GLOBAL: {key!r} not found")
        """,
    dis.opmap[
        "STORE_GLOBAL"
    ]: """
                    if isinstance(names, (list, tuple)):
                        key = names[oparg]
                    else:
                        key = oparg
                    globals_[key] = self.pop()
        """,
    dis.opmap[
        "CALL_FUNCTION"
    ]: """
                    argc = oparg
                    args = [self.pop() for _ in range(argc)][::-1]
                    func = self.pop()
                    result = func(*args)
                    self.push(result)
        """,
    dis.opmap[
        "MAKE_FUNCTION"
    ]: """
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
        """,
    # TODO: DO MORE JUNK SHIT FOR NOP OPCODE
    dis.opmap[
        "NOP"
    ]: """
                    pass
        """,
    dis.opmap[
        "JUMP_FORWARD"
    ]: """
                    self.pc += oparg
        """,
    dis.opmap[
        "JUMP_IF_FALSE_OR_POP"
    ]: """
                    val = self.top()
                    if not val:
                        self.pc = oparg
                    else:
                        self.pop()
        """,
    dis.opmap[
        "JUMP_IF_TRUE_OR_POP"
    ]: """
                    val = self.top()
                    if val:
                        self.pc = oparg
                    else:
                        self.pop()
        """,
    dis.opmap[
        "JUMP_ABSOLUTE"
    ]: """
                    self.pc = oparg
        """,
    dis.opmap[
        "BUILD_TUPLE"
    ]: """
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(tuple(items))
        """,
    dis.opmap[
        "BUILD_LIST"
    ]: """
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(list(items))
        """,
    dis.opmap[
        "BUILD_SET"
    ]: """
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(set(items))
        """,
    dis.opmap[
        "BUILD_MAP"
    ]: """
                    # oparg = number of key-value pairs
                    values = [self.pop() for _ in range(oparg)][::-1]  # pop values in reverse order
                    keys = self.pop()  # keys tuple pushed last
                    if not isinstance(keys, (list, tuple)):
                        raise VMError("BUILD_MAP expects a tuple of keys")
                    d = {key: value for key, value in zip(keys, values)}
                    self.push(d)
        """,
    dis.opmap[
        "EXTENDED_ARG"
    ]: """
                    opcode, oparg = bytecode[self.pc]
                    oparg = (self.extended_arg | (oparg if oparg is not None else 0))
                    self.extended_arg = 0
        """,
    dis.opmap[
        "LOAD_METHOD"
    ]: """
                    if isinstance(names, (list, tuple)):
                        name = names[oparg]
                    elif isinstance(names, dict):
                        name = oparg
                    else:
                        raise VMError("LOAD_METHOD: unexpected names format")

                    obj = self.pop()
                    # Push a tuple (object, method_name) instead of the bound method
                    # CALL_METHOD will handle the actual method call
                    self.push((obj, name))
    """,
    dis.opmap[
        "CALL_METHOD"
    ]: """
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

                    # Try calling
                    try:
                        args = [a.encode("utf-8") if isinstance(a, str) else a.encode("utf-8") for a in args]
                        result = method(*args)
                    except AttributeError:
                        args = [a if isinstance(a, str) else a for a in args]
                        result = method(*args)
                    except Exception as e:
                        print(e)
                        result=None
                    self.push(result)
    """,
    dis.opmap[
        "CALL_FUNCTION_KW"
    ]: """
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
    dis.opmap[
        "CALL_FUNCTION_EX"
    ]: """
                    func = self.stack.pop()
                    args = self.stack.pop()
                    if oparg & 1:
                        kwargs = self.stack.pop()
                        self.stack.append(func(*args, **kwargs))
                    else:
                        self.stack.append(func(*args))
        """,
    dis.opmap[
        "SETUP_FINALLY"
    ]: """
                    # Push the target of finally block onto block stack
                    self.block_stack.append(('finally', self.pc + oparg))
        """,
    dis.opmap[
        "POP_BLOCK"
    ]: """
                    # Pop a block from block stack (no value stack effect)
                    self.block_stack.pop()
        """,
    dis.opmap[
        "POP_EXCEPT"
    ]: """
                    # Pop exception handler (removes type, value, traceback)
                    self.stack.pop(); self.stack.pop(); self.stack.pop()
        """,
    dis.opmap[
        "LOAD_ATTR"
    ]: """
                    # Load attribute from object
                    if isinstance(names, (list, tuple)):
                        name = names[oparg]  # oparg is index
                    elif isinstance(names, dict):
                        name = names.get(oparg)  # map index to actual name
                        if name is None:
                            raise VMError(f"LOAD_ATTR: invalid key {oparg}")
                    else:
                        raise VMError("LOAD_ATTR: unexpected names format")

                    obj = self.pop()
                    self.push(getattr(obj, name))
    """,
    dis.opmap[
        "BUILD_CONST_KEY_MAP"
    ]: """
                    keys = self.pop()  # tuple or list of keys
                    values = [self.pop() for _ in range(oparg)][::-1]
                    # Flatten single-element lists
                    for i in range(len(values)):
                        if isinstance(values[i], list) and len(values[i]) == 1:
                            values[i] = values[i][0]
                    d = dict(zip(keys, values))
                    self.push(d)
        """,
    dis.opmap[
        "SET_UPDATE"
    ]: """
                    # Update a set with multiple items
                    # oparg = number of items
                    items = [self.pop() for _ in range(oparg)][::-1]
                    set_obj = self.pop()
                    set_obj.update(items)
                    self.push(set_obj)
        """,
    dis.opmap[
        "BINARY_AND"
    ]: """
                    b = self.pop()
                    a = self.pop()
                    self.push(a & b)
        """,
    dis.opmap[
        "RAISE_VARARGS"
    ]: """
                    # oparg meanings:
                    # 0: re-raise last exception
                    # 1: raise exception (type or instance) from TOS
                    # 2: raise exception with cause (TOS is cause, TOS1 is exception)
                    if oparg == 0:
                        raise
                    elif oparg == 1:
                        exc = self.pop()
                        raise exc
                    elif oparg == 2:
                        cause = self.pop()
                        exc = self.pop()
                        raise exc from cause
                    else:
                        raise VMError(f"RAISE_VARARGS with invalid oparg {oparg}")
        """,
    dis.opmap[
        "LIST_TO_TUPLE"
    ]: """
                    # Convert list (on TOS) into tuple
                    lst = self.pop()
                    if not isinstance(lst, list):
                        raise VMError("LIST_TO_TUPLE expected a list")
                    self.push(tuple(lst))
        """,
    dis.opmap[
        "INPLACE_LSHIFT"
    ]: """
                    # In-place left shift (a <<= b)
                    b = self.pop()
                    a = self.pop()
                    a <<= b
                    self.push(a)
        """,
    dis.opmap[
        "DELETE_DEREF"
    ]: """
                    # Delete a variable from cell/freevars
                    if isinstance(cells, (list, tuple)):
                        name = cells[oparg]
                    elif isinstance(cells, dict):
                        name = oparg
                    else:
                        raise VMError("DELETE_DEREF: unexpected cells format")

                    try:
                        del self.locals[name]
                    except KeyError:
                        raise NameError(f"free variable {name!r} referenced before assignment in enclosing scope")
        """,
    dis.opmap[
        "YIELD_VALUE"
    ]: """
                    # Yield the top of stack (value to send back to caller)
                    value = self.pop()
                    # In a real VM this would suspend execution, here we just push back
                    return value
            """,
    dis.opmap[
        "COPY_DICT_WITHOUT_KEYS"
    ]: """
                    # Copy dict (TOS1) without specified keys (TOS)
                    keys = self.pop()
                    mapping = self.pop()
                    new_d = {k: v for k, v in mapping.items() if k not in keys}
                    self.push(new_d)
            """,
    dis.opmap[
        "INPLACE_OR"
    ]: """
                    b = self.pop()
                    a = self.pop()
                    a |= b
                    self.push(a)
            """,
    dis.opmap[
        "MATCH_SEQUENCE"
    ]: """
                    # Pushes an iterator for sequence pattern matching
                    seq = self.pop()
                    try:
                        it = iter(seq)
                    except TypeError:
                        raise TypeError(f"object of type {type(seq).__name__!r} is not iterable")
                    self.push(it)
            """,
    dis.opmap[
        "PRINT_EXPR"
    ]: """
                    value = self.pop()
                    if value is not None:
                        print(value)
            """,
    dis.opmap[
        "GET_AITER"
    ]: """
                    # Get asynchronous iterator
                    obj = self.pop()
                    aiter = obj.__aiter__()
                    self.push(aiter)
            """,
    dis.opmap[
        "WITH_EXCEPT_START"
    ]: """
                    # Start handling 'with' exception
                    # TOS: exc_info (type, value, traceback)
                    # TOS1: context manager
                    exc = self.pop()
                    mgr = self.pop()
                    res = mgr.__exit__(*exc)
                    self.push(res)
            """,
    dis.opmap[
        "END_ASYNC_FOR"
    ]: """
                    # Pops 7 values used in async-for finalization
                    for _ in range(7):
                        self.pop()
            """,
    dis.opmap[
        "LOAD_BUILD_CLASS"
    ]: """
                    # Push built-in __build_class__ function
                    self.push(__build_class__)
            """,
    dis.opmap[
        "LOAD_CLASSDEREF"
    ]: """
                    # Load from cell/freevars
                    if isinstance(cells, (list, tuple)):
                        name = cells[oparg]
                    elif isinstance(cells, dict):
                        name = oparg
                    else:
                        raise VMError("LOAD_CLASSDEREF: unexpected cells format")

                    if name in self.locals:
                        self.push(self.locals[name])
                    else:
                        self.push(self.globals.get(name, None))
            """,
    dis.opmap[
        "JUMP_IF_NOT_EXC_MATCH"
    ]: """
                    # If exception does not match expected type, jump to target
                    exc_type = self.pop()
                    err = self.pop()
                    target = oparg
                    if not issubclass(err.__class__, exc_type):
                        self.pc = target
            """,
    dis.opmap[
        "UNPACK_SEQUENCE"
    ]: """
                    # Unpack TOS into oparg items
                    seq = self.pop()
                    if len(seq) != oparg:
                        raise ValueError("UNPACK_SEQUENCE: length mismatch")
                    for item in reversed(seq):
                        self.push(item)
                """,
    dis.opmap[
        "UNPACK_EX"
    ]: """
                    # Unpack with starred expression
                    seq = list(self.pop())
                    before = oparg & 0xFF
                    after = (oparg >> 8)
                    if len(seq) < before + after:
                        raise ValueError("UNPACK_EX: not enough values")
                    for item in reversed(seq[-after:]):
                        self.push(item)
                    self.push(seq[before:len(seq)-after])
                    for item in reversed(seq[:before]):
                        self.push(item)
                """,
    dis.opmap[
        "FORMAT_VALUE"
    ]: """
                    # Format value (used in f-strings)
                    fmt_spec = None
                    if oparg & 0x04:
                        fmt_spec = self.pop()
                    val = self.pop()
                    if oparg & 0x03 == 0:   # no conversion
                        result = str(val)
                    elif oparg & 0x03 == 1: # str()
                        result = str(val)
                    elif oparg & 0x03 == 2: # repr()
                        result = repr(val)
                    elif oparg & 0x03 == 3: # ascii()
                        result = ascii(val)
                    else:
                        raise VMError(f"FORMAT_VALUE: invalid conversion flag {oparg}")
                    if fmt_spec is not None:
                        result = format(result, fmt_spec)
                    self.push(result)
                """,
    dis.opmap[
        "DICT_UPDATE"
    ]: """
                    mapping = self.pop()
                    target = self.stack[-1]
                    if not isinstance(target, dict):
                        raise VMError("DICT_UPDATE target not a dict")
                    target.update(mapping)
                """,
    dis.opmap[
        "INPLACE_POWER"
    ]: """
                    b = self.pop()
                    a = self.pop()
                    self.push(a ** b)
                """,
    dis.opmap[
        "GEN_START"
    ]: """
                    gen = self.stack[-1]
                    if oparg != 0:
                        raise VMError("GEN_START arg must be 0")
                    gen.send(None)
                """,
    dis.opmap[
        "DELETE_FAST"
    ]: """
                    varname = varnames[oparg]
                    try:
                        del names[varname]
                    except KeyError:
                        raise UnboundLocalError(f"local variable {varname!r} not found")
                """,
    dis.opmap[
        "GET_YIELD_FROM_ITER"
    ]: """
                    v = self.stack[-1]
                    if not hasattr(v, "__iter__"):
                        raise VMError("GET_YIELD_FROM_ITER target not iterable")
                    self.stack[-1] = iter(v)
                """,
    dis.opmap[
        "IMPORT_NAME"
    ]: """
                    name = names[oparg] if isinstance(names, (list, tuple)) else oparg
                    fromlist = self.pop()
                    level    = self.pop()
                    module = __import__(name, globals_, names, fromlist, level)
                    self.push(module)
                """,
    dis.opmap[
        "IMPORT_FROM"
    ]: """
                    name = names[oparg] if isinstance(names, (list, tuple)) else oparg
                    module = self.top()
                    self.push(getattr(module, name))
                """,
    dis.opmap[
        "IMPORT_STAR"
    ]: """
                    module = self.pop()
                    for k, v in module.__dict__.items():
                        if not k.startswith("_"):
                            globals_[k] = v
                """,
    dis.opmap[
        "STORE_DEREF"
    ]: """
                    # STORE_DEREF
                    varname = names[oparg]
                    val = self.pop()
                    cells[varname].cell_contents = val
                """,
    dis.opmap[
        "INPLACE_XOR"
    ]: """
                    # INPLACE_XOR
                    b = self.pop()
                    a = self.pop()
                    self.push(a ^ b)
                """,
    dis.opmap[
        "STORE_SUBSCR"
    ]: """
                    # STORE_SUBSCR
                    value = self.pop()
                    index = self.pop()
                    target = self.pop()
                    target[index] = value
                """,
    dis.opmap[
        "MATCH_MAPPING"
    ]: """
                    # MATCH_MAPPING
                    self.push(True)  # Placeholder for pattern matching
                """,
    dis.opmap[
        "BUILD_STRING"
    ]: """
                    # BUILD_STRING
                    pieces = [self.pop() for _ in range(oparg)][::-1]
                    self.push(''.join(map(str, pieces)))
                """,
    dis.opmap[
        "BINARY_XOR"
    ]: """
                    # BINARY_XOR
                    b = self.pop()
                    a = self.pop()
                    self.push(a ^ b)
                """,
    dis.opmap[
        "LOAD_ASSERTION_ERROR"
    ]: """
                    # LOAD_ASSERTION_ERROR
                    self.push(AssertionError)
                """,
    dis.opmap[
        "LIST_EXTEND"
    ]: """
                    # LIST_EXTEND
                    iterable = self.pop()
                    target = self.stack[-1]
                    target.extend(iterable)
                """,
    dis.opmap[
        "DELETE_NAME"
    ]: """
                    # DELETE_NAME
                    varname = names[oparg]
                    if varname in globals_:
                        del globals_[varname]
                """,
    dis.opmap[
        "ROT_FOUR"
    ]: """
                    # ROT_FOUR
                    a = self.pop()
                    b = self.pop()
                    c = self.pop()
                    d = self.pop()
                    self.push(b)
                    self.push(a)
                    self.push(d)
                    self.push(c)
                """,
    dis.opmap[
        "BINARY_OR"
    ]: """
                    b = self.pop()
                    a = self.pop()
                    self.push(a | b)
                """,
    dis.opmap[
        "CONTAINS_OP"
    ]: """
                    container = self.pop()
                    value = self.pop()
                    self.push(value in container)  # simplified
                """,
    dis.opmap[
        "DUP_TOP"
    ]: """
                    self.push(self.stack[-1])
                """,
    dis.opmap[
        "DUP_TOP_TWO"
    ]: """
                    self.push(self.stack[-2])
                    self.push(self.stack[-1])
                """,
    dis.opmap[
        "LOAD_DEREF"
    ]: """
                    self.push(self.closure[oparg])  # simplified
                """,
    dis.opmap[
        "MAP_ADD"
    ]: """
                    value = self.pop()
                    key = self.pop()
                    mapping = self.pop()
                    mapping[key] = value
                    self.push(mapping)
                """,
    dis.opmap[
        "ROT_N"
    ]: """
                    n = oparg
                    self.stack[-n:] = [self.stack[-1]] + self.stack[-n:-1]
                """,
    dis.opmap[
        "ROT_THREE"
    ]: """
                    self.stack[-3], self.stack[-2], self.stack[-1] = self.stack[-2], self.stack[-1], self.stack[-3]
                """,
    dis.opmap[
        "ROT_TWO"
    ]: """
                self.stack[-2], self.stack[-1] = self.stack[-1], self.stack[-2]
                """,
    dis.opmap[
        "SETUP_ANNOTATIONS"
    ]: """
                self.push({})
                """,
    dis.opmap[
        "UNARY_NEGATIVE"
    ]: """
                self.push(-self.pop())
                """,
    dis.opmap[
        "UNARY_NOT"
    ]: """
                self.push(not self.pop())
                """,
    dis.opmap[
        "YIELD_FROM"
    ]: """
                self.push(self.pop())  # simplified; real behavior yields from a generator
                """,
    dis.opmap[
        "GET_AWAITABLE"
    ]: """
                    # GET_AWAITABLE
                    awaitable = self.pop()
                    self.push(awaitable)  # Placeholder: no async handling
                """,
    dis.opmap[
        "SET_ADD"
    ]: """
                    # SET_ADD
                    value = self.pop()
                    target_set = self.stack[-1]
                    target_set.add(value)
                """,
    dis.opmap[
        "UNARY_INVERT"
    ]: """
                    # UNARY_INVERT
                    a = self.pop()
                    self.push(~a)
                """,
    dis.opmap[
        "BINARY_LSHIFT"
    ]: """
                    # BINARY_LSHIFT
                    b = self.pop()
                    a = self.pop()
                    self.push(a << b)
                """,
    dis.opmap[
        "FOR_ITER"
    ]: """
                    # FOR_ITER
                    try:
                        value = next(self.stack[-1])
                        self.push(value)
                    except StopIteration:
                        self.jump(oparg)
                """,
    dis.opmap[
        "UNARY_POSITIVE"
    ]: """
                    # Unary positive: +x
                    x = self.pop()
                    self.push(+x)
                    """,
    dis.opmap[
        "BINARY_RSHIFT"
    ]: """
                    # Binary right shift: x >> y
                    right = self.pop()
                    left = self.pop()
                    self.push(left >> right)
                    """,
    dis.opmap[
        "INPLACE_MODULO"
    ]: """
                    # In-place modulo: x %= y
                    right = self.pop()
                    left = self.pop()
                    self.push(left % right)
                    """,
    dis.opmap[
        "STORE_ATTR"
    ]: """
                    # Store attribute: obj.name = value
                    value = self.pop()
                    obj = self.pop()
                    name = self.names[oparg] if isinstance(self.names, (list, tuple)) else oparg
                    setattr(obj, name, value)
                    """,
    dis.opmap[
        "DELETE_ATTR"
    ]: """
                    # Delete attribute: del obj.name
                    obj = self.pop()
                    name = self.names[oparg] if isinstance(self.names, (list, tuple)) else oparg
                    delattr(obj, name)
                    """,
    dis.opmap[
        "DELETE_GLOBAL"
    ]: """
                    # Delete a global variable
                    name = self.names[oparg] if isinstance(self.names, (list, tuple)) else oparg
                    del self.globals[name]
                    """,
    dis.opmap[
        "RERAISE"
    ]: """
                    # Re-raise exception
                    exc = self.pop()
                    self.push(exc)
                    raise exc
                    """,
    # dis.opmap[
    #     "GET_ANEXT"
    # ]: """
    #                 # Async iterator: await anext(obj)
    #                 aiter = self.pop()
    #                 self.push(await aiter.__anext__())
    #                 """,
    dis.opmap[
        "MATCH_KEYS"
    ]: """
                    # Pattern matching keys
                    subject = self.pop()
                    keys = self.pop()
                    matches = all(k in subject for k in keys)
                    self.push(matches)
                    """,
    dis.opmap[
        "SETUP_WITH"
    ]: """
                    # Context manager setup
                    manager = self.pop()
                    enter = manager.__enter__()
                    self.push(manager)
                    self.push(enter)
                    """,
    # dis.opmap[
    #     "SETUP_ASYNC_WITH"
    # ]: """
    #                 # Async context manager setup
    #                 manager = await self.pop().__aenter__()
    #                 self.push(manager)
    #                 """,
    dis.opmap[
        "MATCH_CLASS"
    ]: """
                    # Match class opcode (simplified)
                    cls = self.pop()
                    obj = self.pop()
                    self.push(isinstance(obj, cls))
                    """,
    dis.opmap[
        "BEFORE_ASYNC_WITH"
    ]: """
                    # BEFORE_ASYNC_WITH: Prepare async context manager
                    manager = self.pop()
                    self.push(manager)
                    """,
    dis.opmap[
        "BINARY_MATRIX_MULTIPLY"
    ]: """
                    # Binary matrix multiply: x @ y
                    right = self.pop()
                    left = self.pop()
                    self.push(left @ right)
                    """,
    dis.opmap[
        "BUILD_SLICE"
    ]: """
                    # Build a slice object
                    if oparg == 2:
                        stop = self.pop()
                        start = self.pop()
                        self.push(slice(start, stop))
                    elif oparg == 3:
                        step = self.pop()
                        stop = self.pop()
                        start = self.pop()
                        self.push(slice(start, stop, step))
                    """,
    dis.opmap[
        "DELETE_SUBSCR"
    ]: """
                    # Delete subscription: del obj[key]
                    key = self.pop()
                    obj = self.pop()
                    del obj[key]
                    """,
    dis.opmap[
        "DICT_MERGE"
    ]: """
                    # Merge dictionaries
                    other = self.pop()
                    target = self.pop()
                    target.update(other)
                    self.push(target)
                    """,
    dis.opmap[
        "GET_ITER"
    ]: """
                    # Get iterator
                    iterable = self.pop()
                    self.push(iter(iterable))
                    """,
    dis.opmap[
        "INPLACE_ADD"
    ]: """
                    # In-place addition: x += y
                    right = self.pop()
                    left = self.pop()
                    self.push(left + right)
                    """,
    dis.opmap[
        "INPLACE_AND"
    ]: """
                    # In-place AND: x &= y
                    right = self.pop()
                    left = self.pop()
                    self.push(left & right)
                    """,
    dis.opmap[
        "INPLACE_MATRIX_MULTIPLY"
    ]: """
                    # In-place matrix multiply: x @= y
                    right = self.pop()
                    left = self.pop()
                    self.push(left @ right)
                    """,
    dis.opmap[
        "INPLACE_MULTIPLY"
    ]: """
                    # In-place multiply: x *= y
                    right = self.pop()
                    left = self.pop()
                    self.push(left * right)
                    """,
    dis.opmap[
        "INPLACE_RSHIFT"
    ]: """
                    # In-place right shift: x >>= y
                    right = self.pop()
                    left = self.pop()
                    self.push(left >> right)
                    """,
    dis.opmap[
        "INPLACE_SUBTRACT"
    ]: """
                    # In-place subtraction: x -= y
                    right = self.pop()
                    left = self.pop()
                    self.push(left - right)
                    """,
    dis.opmap[
        "IS_OP"
    ]: """
                    # IS_OP: checks 'is' or 'is not'
                    right = self.pop()
                    left = self.pop()
                    if oparg == 0:
                        self.push(left is right)
                    elif oparg == 1:
                        self.push(left is not right)
                    """,
    dis.opmap[
        "LIST_APPEND"
    ]: """
                    # Append to list at index oparg
                    value = self.pop()
                    lst = self.stack[-oparg]
                    lst.append(value)
                    """,
    dis.opmap[
        "LOAD_CLOSURE"
    ]: """
                    # Load closure cell
                    self.push(self.cells[oparg])
                    """,
}
