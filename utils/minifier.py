"""
pyminify.py — a Python minifier utility (importable, not CLI)

Features:
- strip comments and docstrings
- trim blank lines
- optional local variable/argument name mangling (experimental)

Requires Python 3.9+ (uses ast.unparse).
"""
import ast
from typing import List, Dict, Set

class _StripDocstringsAndMangle(ast.NodeTransformer):
    def __init__(self, mangle: bool = False):
        super().__init__()
        self.mangle = mangle
        self._counter = 0

    def _new_name(self) -> str:
        name = f"_{self._counter}"
        self._counter += 1
        return name

    @staticmethod
    def _is_docstring_stmt(node: ast.stmt) -> bool:
        return (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        )

    def visit_Module(self, node: ast.Module):
        self.generic_visit(node)
        if node.body and self._is_docstring_stmt(node.body[0]):
            node.body.pop(0)
        return node

    def visit_ClassDef(self, node: ast.ClassDef):
        self.generic_visit(node)
        if node.body and self._is_docstring_stmt(node.body[0]):
            node.body.pop(0)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.generic_visit(node)
        if node.body and self._is_docstring_stmt(node.body[0]):
            node.body.pop(0)
        if self.mangle:
            return self._mangle_function(node)
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.generic_visit(node)
        if node.body and self._is_docstring_stmt(node.body[0]):
            node.body.pop(0)
        if self.mangle:
            return self._mangle_function(node)
        return node

    def _collect_local_names(self, node: ast.FunctionDef) -> Set[str]:
        local: Set[str] = set()

        for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
            local.add(arg.arg)
        if node.args.vararg:
            local.add(node.args.vararg.arg)
        if node.args.kwarg:
            local.add(node.args.kwarg.arg)

        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.names: Set[str] = set()
            def visit_Name(self, n: ast.Name):
                if isinstance(n.ctx, ast.Store):
                    self.names.add(n.id)

        f = Finder()
        for stmt in node.body:
            f.visit(stmt)

        local.update(f.names)
        local.discard("self")
        return local

    def _mangle_function(self, node: ast.FunctionDef):
        local_names = self._collect_local_names(node)
        if not local_names:
            return node

        mapping: Dict[str, str] = {name: self._new_name() for name in sorted(local_names)}

        class Renamer(ast.NodeTransformer):
            def visit_Name(self, n: ast.Name):
                if n.id in mapping:
                    return ast.copy_location(ast.Name(id=mapping[n.id], ctx=n.ctx), n)
                return n
            def visit_arg(self, a: ast.arg):
                if a.arg in mapping:
                    return ast.copy_location(ast.arg(arg=mapping[a.arg], annotation=a.annotation), a)
                return a

        r = Renamer()
        new_node = r.visit(node)
        ast.fix_missing_locations(new_node)
        return new_node

def minify_source(src: str, *, mangle: bool = False) -> str:
    """
    Minify Python source.
    - strip docstrings and comments
    - trim blank lines
    - optional mangle local names
    """
    tree = ast.parse(src)
    tree = _StripDocstringsAndMangle(mangle=mangle).visit(tree)
    ast.fix_missing_locations(tree)

    try:
        out = ast.unparse(tree)
    except AttributeError:
        raise RuntimeError("ast.unparse requires Python 3.9+")

    lines = out.splitlines()
    cleaned: List[str] = []
    prev_blank = False
    for ln in lines:
        ln = ln.rstrip()
        if not ln:
            if not prev_blank:
                cleaned.append("")
            prev_blank = True
        else:
            cleaned.append(ln)
            prev_blank = False
    return "\n".join(cleaned) + "\n"
