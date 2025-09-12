# 3.11
import dis
import operator

BINARY_OPERATORS = {
    0: operator.add,
    1: operator.sub,
    2: operator.mul,
    3: operator.matmul,
    4: operator.truediv,
    5: operator.mod,
    6: operator.floordiv,
    7: operator.pow,
    8: operator.lshift,
    9: operator.rshift,
    10: operator.and_,
    11: operator.or_,
    12: operator.xor,
    13: operator.eq,
    14: operator.ne,
    15: operator.lt,
    16: operator.le,
    17: operator.gt,
    18: operator.ge,
    19: lambda a, b: a in b,
    20: lambda a, b: a not in b,
    21: operator.is_,
    22: operator.is_not,
    23: lambda a, b: isinstance(a, b),  # exception match placeholder
}
OP_HANDLERS={
    dis.opmap["IS_OP" ]: """
                    # IS_OP: checks 'is' or 'is not'
                    right = self.pop()
                    left = self.pop()
                    if oparg == 0:
                        self.push(left is right)
                    elif oparg == 1:
                        self.push(left is not right)
                    """,
    dis.opmap["LIST_APPEND" ]: """
                    # Append to list at index oparg
                    value = self.pop()
                    lst = self.stack[-oparg]
                    lst.append(value)
                    """,
    dis.opmap["LOAD_CLOSURE" ]: """
                    # Load closure cell
                    self.push(self.cells[oparg])
                    """,
    dis.opmap["DICT_MERGE" ]: """
                    # Merge dictionaries
                    other = self.pop()
                    target = self.pop()
                    target.update(other)
                    self.push(target)
                    """,
    dis.opmap["GET_ITER" ]: """
                    # Get iterator
                    iterable = self.pop()
                    self.push(iter(iterable))
                    """,
    dis.opmap["BUILD_SLICE" ]: """
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
    dis.opmap["DELETE_SUBSCR" ]: """
                    # Delete subscription: del obj[key]
                    key = self.pop()
                    obj = self.pop()
                    del obj[key]
                    """,
    dis.opmap["MATCH_CLASS" ]: """
                    # Match class opcode (simplified)
                    cls = self.pop()
                    obj = self.pop()
                    self.push(isinstance(obj, cls))
                    """,
    dis.opmap["BEFORE_ASYNC_WITH" ]: """
                    # BEFORE_ASYNC_WITH: Prepare async context manager
                    manager = self.pop()
                    self.push(manager)
                    """,
    dis.opmap["STORE_ATTR" ]: """
                    # Store attribute: obj.name = value
                    value = self.pop()
                    obj = self.pop()
                    name = self.names[oparg] if isinstance(self.names, (list, tuple)) else oparg
                    setattr(obj, name, value)
                    """,
    dis.opmap["DELETE_ATTR" ]: """
                    # Delete attribute: del obj.name
                    obj = self.pop()
                    name = self.names[oparg] if isinstance(self.names, (list, tuple)) else oparg
                    delattr(obj, name)
                    """,
    dis.opmap["DELETE_GLOBAL" ]: """
                    # Delete a global variable
                    name = self.names[oparg] if isinstance(self.names, (list, tuple)) else oparg
                    del self.globals[name]
                    """,
    dis.opmap["RERAISE" ]: """
                    # Re-raise exception
                    exc = self.pop()
                    self.push(exc)
                    raise exc
                    """,
    dis.opmap["FOR_ITER" ]: """
                    # FOR_ITER
                    try:
                        value = next(self.stack[-1])
                        self.push(value)
                    except StopIteration:
                        self.jump(oparg)
                """,
    dis.opmap["UNARY_POSITIVE" ]: """
                    # Unary positive: +x
                    x = self.pop()
                    self.push(+x)
                    """,
    dis.opmap["UNARY_NEGATIVE" ]: """
                    self.push(-self.pop())
                """,
    dis.opmap["UNARY_NOT" ]: """
                    self.push(not self.pop())
                """,
    dis.opmap["GET_AWAITABLE" ]: """
                    # GET_AWAITABLE
                    awaitable = self.pop()
                    self.push(awaitable)  # Placeholder: no async handling
                """,
    dis.opmap["SET_ADD" ]: """
                    # SET_ADD
                    value = self.pop()
                    target_set = self.stack[-1]
                    target_set.add(value)
                """,
    dis.opmap["UNARY_INVERT" ]: """
                    # UNARY_INVERT
                    a = self.pop()
                    self.push(~a)
                """,
    dis.opmap["CONTAINS_OP" ]: """
                    container = self.pop()
                    value = self.pop()
                    self.push(value in container)  # simplified
                """,
    dis.opmap["LOAD_DEREF" ]: """
                    self.push(self.closure[oparg])  # simplified
                """,
    dis.opmap["MAP_ADD" ]: """
                    value = self.pop()
                    key = self.pop()
                    mapping = self.pop()
                    mapping[key] = value
                    self.push(mapping)
                """,
    dis.opmap["SETUP_ANNOTATIONS" ]: """
                    self.push({})
                """,
    dis.opmap["LOAD_ASSERTION_ERROR" ]: """
                    # LOAD_ASSERTION_ERROR
                    self.push(AssertionError)
                """,
    dis.opmap["LIST_EXTEND" ]: """
                    # LIST_EXTEND
                    iterable = self.pop()
                    target = self.stack[-1]
                    target.extend(iterable)
                """,
    dis.opmap["DELETE_NAME" ]: """
                    # DELETE_NAME
                    varname = names[oparg]
                    if varname in globals_:
                        del globals_[varname]
                """,
    dis.opmap["STORE_SUBSCR" ]: """
                    # STORE_SUBSCR
                    value = self.pop()
                    index = self.pop()
                    target = self.pop()
                    target[index] = value
                """,
    dis.opmap["MATCH_MAPPING" ]: """
                    # MATCH_MAPPING
                    self.push(True)  # Placeholder for pattern matching
                """,
    dis.opmap["BUILD_STRING" ]: """
                    # BUILD_STRING
                    pieces = [self.pop() for _ in range(oparg)][::-1]
                    self.push(''.join(map(str, pieces)))
                """,
    dis.opmap["DELETE_FAST" ]: """
                    varname = varnames[oparg]
                    try:
                        del names[varname]
                    except KeyError:
                        raise UnboundLocalError(f"local variable {varname!r} not found")
                """,
    dis.opmap["GET_YIELD_FROM_ITER" ]: """
                    v = self.stack[-1]
                    if not hasattr(v, "__iter__"):
                        raise VMError("GET_YIELD_FROM_ITER target not iterable")
                    self.stack[-1] = iter(v)
                """,
    dis.opmap["IMPORT_NAME" ]: """
                    name = names[oparg] if isinstance(names, (list, tuple)) else oparg
                    fromlist = self.pop()
                    level    = self.pop()
                    module = __import__(name, globals_, names, fromlist, level)
                    self.push(module)
                """,
    dis.opmap["IMPORT_FROM" ]: """
                    name = names[oparg] if isinstance(names, (list, tuple)) else oparg
                    module = self.top()
                    self.push(getattr(module, name))
                """,
    dis.opmap["IMPORT_STAR" ]: """
                    module = self.pop()
                    for k, v in module.__dict__.items():
                        if not k.startswith("_"):
                            globals_[k] = v
                """,
    dis.opmap["STORE_DEREF" ]: """
                    # STORE_DEREF
                    varname = names[oparg]
                    val = self.pop()
                    cells[varname].cell_contents = val
                """,
    dis.opmap["UNPACK_SEQUENCE" ]: """
                    # Unpack TOS into oparg items
                    seq = self.pop()
                    if len(seq) != oparg:
                        raise ValueError("UNPACK_SEQUENCE: length mismatch")
                    for item in reversed(seq):
                        self.push(item)
                """,
    dis.opmap["UNPACK_EX" ]: """
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
    dis.opmap["FORMAT_VALUE" ]: """
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
    dis.opmap["DICT_UPDATE"]: """
                    mapping = self.pop()
                    target = self.pop()
                    if not isinstance(target, dict):
                        raise VMError("DICT_UPDATE target not a dict")
                    target.update(mapping)
                    self.push(target)
                """,
    dis.opmap["END_ASYNC_FOR" ]: """
                    # Pops 7 values used in async-for finalization
                    for _ in range(7):
                        self.pop()
            """,
    dis.opmap["LOAD_BUILD_CLASS" ]: """
                    # Push built-in __build_class__ function
                    self.push(__build_class__)
            """,
    dis.opmap["LOAD_CLASSDEREF" ]: """
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
    dis.opmap["MATCH_SEQUENCE" ]: """
                    # Pushes an iterator for sequence pattern matching
                    seq = self.pop()
                    try:
                        it = iter(seq)
                    except TypeError:
                        raise TypeError(f"object of type {type(seq).__name__!r} is not iterable")
                    self.push(it)
            """,
    dis.opmap["PRINT_EXPR" ]: """
                    value = self.pop()
                    if value is not None:
                        print(value)
            """,
    dis.opmap["GET_AITER" ]: """
                    obj = self.pop()
                    self.push(obj.__aiter__())
            """,
    dis.opmap["WITH_EXCEPT_START" ]: """
                    # Start handling 'with' exception
                    # TOS: exc_info (type, value, traceback)
                    # TOS1: context manager
                    exc = self.pop()
                    mgr = self.pop()
                    res = mgr.__exit__(*exc)
                    self.push(res)
            """,
    dis.opmap["DELETE_DEREF" ]: """
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
    dis.opmap["YIELD_VALUE" ]: """
                    # Yield the top of stack (value to send back to caller)
                    value = self.pop()
                    # In a real VM this would suspend execution, here we just push back
                    return value
            """,
    dis.opmap["RAISE_VARARGS" ]: """
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
    dis.opmap["LIST_TO_TUPLE" ]: """
                    # Convert list (on TOS) into tuple
                    lst = self.pop()
                    if not isinstance(lst, list):
                        raise VMError("LIST_TO_TUPLE expected a list")
                    self.push(tuple(lst))
        """,

    dis.opmap["POP_EXCEPT" ]: """
                    # Pop exception handler (removes type, value, traceback)
                    self.stack.pop(); self.stack.pop(); self.stack.pop()
        """,
    dis.opmap["LOAD_ATTR" ]: """
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
    dis.opmap["BUILD_CONST_KEY_MAP" ]: """
                    keys = self.pop()  # tuple or list of keys
                    values = [self.pop() for _ in range(oparg)][::-1]
                    # Flatten single-element lists
                    for i in range(len(values)):
                        if isinstance(values[i], list) and len(values[i]) == 1:
                            values[i] = values[i][0]
                    d = dict(zip(keys, values))
                    self.push(d)
        """,
    dis.opmap["SET_UPDATE" ]: """
                    # Update a set with multiple items
                    # oparg = number of items
                    items = [self.pop() for _ in range(oparg)][::-1]
                    set_obj = self.pop()
                    set_obj.update(items)
                    self.push(set_obj)
        """,
    dis.opmap["CALL_FUNCTION_EX"]: """
                    # Pop the callable and arguments
                    func = self.stack.pop()
                    args = self.stack.pop()  # tuple/list of positional arguments

                    # If func is old-style function with __globals__, update globals
                    if hasattr(func, "__globals__") and self.globals is not None:
                        func.__globals__.update(self.globals)

                    # If **kwargs are present (oparg & 1)
                    if oparg & 1:
                        kwargs = self.stack.pop()
                        if not isinstance(kwargs, dict):
                            kwargs = dict(kwargs)
                    else:
                        kwargs = {}

                    # Ensure args is iterable
                    if not isinstance(args, (tuple, list)):
                        args = [args]

                    # Call safely
                    try:
                        result = func(*args, **kwargs)
                    except Exception as e:
                        print(f"[CALL_FUNCTION_EX error] {e}")
                        result = None

                    self.stack.append(result)
    """,
    dis.opmap["BUILD_TUPLE" ]: """
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(tuple(items))
        """,
    dis.opmap["BUILD_LIST" ]: """
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(list(items))
        """,
    dis.opmap["BUILD_SET" ]: """
                    items = [self.pop() for _ in range(oparg)][::-1]
                    self.push(set(items))
        """,
    dis.opmap["BUILD_MAP" ]: """
                    d = {}
                    for _ in range(oparg):
                        value = self.pop()
                        key = self.pop()
                        d[key] = value
                    self.push(d)
        """,
    dis.opmap["EXTENDED_ARG" ]: """
                    opcode, oparg = bytecode[self.pc]
                    oparg = (self.extended_arg | (oparg if oparg is not None else 0))
                    self.extended_arg = 0
        """,
    dis.opmap["JUMP_FORWARD" ]: """
                    self.pc += oparg
        """,
    dis.opmap["JUMP_IF_FALSE_OR_POP" ]: """
                    val = self.top()
                    if not val:
                        self.pc = oparg
                    else:
                        self.pop()
        """,
    dis.opmap["JUMP_IF_TRUE_OR_POP" ]: """
                    val = self.top()
                    if val:
                        self.pc = oparg
                    else:
                        self.pop()
        """,
    dis.opmap["NOP" ]: """
                    pass
        """,
    dis.opmap["MAKE_FUNCTION" ]: """
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
    dis.opmap["LOAD_NAME" ]: """
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
    dis.opmap["STORE_NAME" ]: """
                    if isinstance(names, (list, tuple)):
                        key = names[oparg]
                    else:
                        key = str(oparg)

                    if not self.stack:  # safeguard
                        raise VMError(f"STORE_NAME: empty stack, cannot assign to {key!r}")

                    value = self.pop()
                    self.globals[key] = value

        """,
    dis.opmap["LOAD_GLOBAL" ]: """
                    if isinstance(names, (list, tuple)):
                        key = names[oparg]
                    else:
                        key = oparg
                    if key in globals_:
                        self.push(globals_[key])
                    else:
                        raise VMError(f"LOAD_GLOBAL: {key!r} not found")
        """,
    dis.opmap["STORE_GLOBAL" ]: """
                    if isinstance(names, (list, tuple)):
                        key = names[oparg]
                    else:
                        key = oparg
                    globals_[key] = self.pop()
        """,
    dis.opmap["POP_JUMP_FORWARD_IF_FALSE" ]: """
                    val = self.pop()
                    if not val:
                        self.pc = oparg """,
    dis.opmap["POP_JUMP_FORWARD_IF_TRUE" ]: """
                    val = self.pop()
                    if val: 
                        self.pc = oparg
        """,
    dis.opmap["POP_JUMP_FORWARD_IF_NOT_NONE" ]: """
                    val = self.pop()
                    if val is not None:
                        self.pc = oparg """,
    dis.opmap["POP_JUMP_FORWARD_IF_NONE" ]: """
                    val = self.pop()
                    if val is None: 
                        self.pc = oparg
        """,
    dis.opmap["RETURN_VALUE"]: """ return self.pop() """,
    dis.opmap["COMPARE_OP" ]: """
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
    dis.opmap["GET_LEN" ]: """
                    a = self.pop(); self.push(len(a))
        """,
    dis.opmap["POP_TOP"]: """ self.pop() """,
    dis.opmap["LOAD_CONST"]: """ self.push(consts[oparg]) """,
    # STORE_FAST
    dis.opmap["STORE_FAST" ]: """
                    if not hasattr(self, "locals"):
                        self.locals = {}
                    varname = varnames[oparg] if isinstance(varnames, (list, tuple)) else str(oparg)
                    value = self.pop()
                    self.locals[varname] = value
        """,
    # LOAD_FAST
    dis.opmap["LOAD_FAST" ]: """
                    if not hasattr(self, "locals"):
                        self.locals = {}
                    varname = varnames[oparg] if isinstance(varnames, (list, tuple)) else str(oparg)
                    if varname not in self.locals:
                        raise UnboundLocalError(f"local variable {varname!r} referenced before assignment")
                    self.push(self.locals[varname])
        """,
    dis.opmap["LOAD_CONST" ]: """
                    value = consts[oparg]
                    self.push(value)
        """,        
    dis.opmap["RETURN_VALUE" ]: """
                    return self.pop()
        """,
    dis.opmap["ASYNC_GEN_WRAP"]: """
                    # ASYNC_GEN_WRAP: stack effect 0
                    pass
    """,

    dis.opmap["BEFORE_WITH"]: """
        # BEFORE_WITH: stack effect +1
                    self.push(None)
    """,

    dis.opmap["BINARY_OP"]: r"""
                    right = self.pop()
                    left = self.pop()
                    if left is None or right is None:
                        raise RuntimeError(f"Cannot perform {oparg} on left={left} right={right}")
                    if oparg == 0:
                        self.push(left + right)
                    elif oparg == 1:
                        self.push(left - right)
                    elif oparg == 2:
                        self.push(left * right)
                    elif oparg == 3:
                        self.push(left @ right)
                    elif oparg == 4:
                        self.push(left / right)
                    elif oparg == 5:
                        self.push(left % right)
                    elif oparg == 6:
                        self.push(left // right)
                    elif oparg == 7:
                        self.push(left ** right)
                    elif oparg == 8:
                        self.push(left << right)
                    elif oparg == 9:
                        self.push(left >> right)
                    elif oparg == 10:
                        self.push(left & right)
                    elif oparg == 11:
                        self.push(left | right)
                    elif oparg == 12:
                        self.push(left ^ right)
                    elif oparg == 13:
                        self.push(left == right)
                    elif oparg == 14:
                        self.push(left != right)
                    elif oparg == 15:
                        self.push(left < right)
                    elif oparg == 16:
                        self.push(left <= right)
                    elif oparg == 17: 
                        self.push(left > right)
                    elif oparg == 18: 
                        self.push(left >= right)
                    elif oparg == 19:
                        self.push(left in right)
                    elif oparg == 20: 
                        self.push(left not in right)
                    elif oparg == 21: 
                        self.push(left is right)
                    elif oparg == 22:
                        self.push(left is not right)
                    elif oparg == 23:
                        self.push(isinstance(left, right))
                    else:
                        raise RuntimeError(f"Unsupported BINARY_OP oparg: {oparg}")
    """,

    dis.opmap["BINARY_SUBSCR"]: """
                    # BINARY_SUBSCR: stack effect -1
                    key = self.pop()
                    container = self.pop()
                    self.push(container[key])
    """,

    dis.opmap["CACHE"]: """
                    # CACHE: stack effect 0
                    pass
    """,
    dis.opmap["CALL"]: """
                    arg1=self.pop()
                    if callable(arg1):
                        args = [self.pop() for _ in range(oparg-1)]
                        func = arg1
                    else:
                        args = [self.pop() for _ in range(oparg-1)] + [arg1]
                        func = self.pop()
                    
                    
                        
                    # Call the function with its arguments and push the result
                    self.push(func(*args))
    """,

    dis.opmap["CHECK_EG_MATCH"]: """
                    # CHECK_EG_MATCH: stack effect 0
                    pass
    """,

    dis.opmap["CHECK_EXC_MATCH"]: """
                    # CHECK_EXC_MATCH: stack effect 0
                    pass
    """,

    dis.opmap["COPY"]: """
                    # COPY: stack effect +1
                    self.push(self.stack[-oparg])
    """,

    dis.opmap["COPY_FREE_VARS"]: """
                    # COPY_FREE_VARS: stack effect 0
                    pass
    """,

    dis.opmap["GET_ANEXT"]: """
                    # GET_ANEXT: stack effect +1
                    iterator = self.pop()
                    self.push(next(iterator, None))
    """,

    dis.opmap["JUMP_BACKWARD"]: """
                    # JUMP_BACKWARD: stack effect 0
                    self.pc -= oparg
    """,

    dis.opmap["JUMP_BACKWARD_NO_INTERRUPT"]: """
                    # JUMP_BACKWARD_NO_INTERRUPT: stack effect 0
                    self.pc -= oparg
    """,

    dis.opmap["KW_NAMES"]: """
                    # KW_NAMES: stack effect 0
                    pass
    """,

    dis.opmap["LOAD_METHOD"]: """
                    # LOAD_METHOD: stack effect +1
                    obj = self.pop()
                    method = getattr(obj, self.names[oparg])
                    self.push(method)
    """,

    dis.opmap["MAKE_CELL"]: """
                    # MAKE_CELL: stack effect 0
                    self.push(Cell(self.pop()))
    """,

    dis.opmap["MATCH_KEYS"]: """
                    # MATCH_KEYS: extracts values from a mapping for pattern matching
                    keys = self.pop()        # a tuple/list of keys from the pattern
                    mapping = self.pop()     # the dict/object to match against
                    result = tuple(mapping[k] for k in keys)
                    self.push(result)
    """,

    dis.opmap["POP_JUMP_BACKWARD_IF_FALSE"]: """
                    # POP_JUMP_BACKWARD_IF_FALSE: stack effect -1
                    value = self.pop()
                    if not value:
                        self.pc -= oparg
    """,

    dis.opmap["POP_JUMP_BACKWARD_IF_NONE"]: """
                    # POP_JUMP_BACKWARD_IF_NONE: stack effect -1
                    value = self.pop()
                    if value is None:
                        self.pc -= oparg
    """,

    dis.opmap["POP_JUMP_BACKWARD_IF_NOT_NONE"]: """
                    # POP_JUMP_BACKWARD_IF_NOT_NONE: stack effect -1
                    value = self.pop()
                    if value is not None:
                        self.pc -= oparg
    """,

    dis.opmap["POP_JUMP_BACKWARD_IF_TRUE"]: """
                    # POP_JUMP_BACKWARD_IF_TRUE: stack effect -1
                    value = self.pop()
                    if value:
                        self.pc -= oparg
    """,

    dis.opmap["PRECALL"]: """
                    # PRECALL: stack effect 0
                    pass
    """,

    dis.opmap["PREP_RERAISE_STAR"]: """
                    # PREP_RERAISE_STAR: stack effect -1
                    self.pop()
    """,

    dis.opmap["PUSH_EXC_INFO"]: """
                    # PUSH_EXC_INFO: pushes current exception info (type, value, traceback)
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    self.push((exc_type, exc_value, exc_tb))
    """,

    dis.opmap["PUSH_NULL"]: """
                    # PUSH_NULL: stack effect +1
                    self.push(None)
    """,

    dis.opmap["RESUME"]: """
                    # RESUME: stack effect 0
                    pass
    """,

    dis.opmap["RETURN_GENERATOR"]: """
                    # RETURN_GENERATOR: stack effect 0
                    return GeneratorExit()
    """,

    dis.opmap["SEND"]: """
                    # SEND: stack effect 0
                    value = self.pop()
                    gen = self.pop()
                    self.push(gen.send(value))
    """,

    dis.opmap["SWAP"]: """
                    # SWAP: stack effect 0
                    i = -oparg - 1
                    self.stack[i], self.stack[-1] = self.stack[-1], self.stack[i]
    """
}
