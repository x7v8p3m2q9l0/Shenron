import ast,random
def var_con_cak():
    return ''.join(random.choices([chr(i) for i in range(44032, 55204) if chr(i).isprintable() and chr(i).isidentifier()], k=11))

class ObfuscatorV2(ast.NodeTransformer):
    def __init__(self):
        # Maps old variable/class names to new names
        self.name_map = {}

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Finds and renames class definitions."""
        original_name = node.name
        if original_name not in self.name_map:
            new_name = var_con_cak()
            self.name_map[original_name] = new_name
        
        node.name = self.name_map[original_name]
        self.generic_visit(node)
        return node

    # def visit_Assign(self, node: ast.Assign) -> ast.Assign:
    #     """Finds assignments of constant values and renames the variable."""
    #     # Handles simple assignments: NAME = value
    #     if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            
    #         # **IMPROVEMENT**: Check for more types of constants, not just simple ones.
    #         constant_types = (ast.Constant, ast.List, ast.Tuple, ast.Dict)
            
    #         if isinstance(node.value, constant_types):
    #             var_name_node = node.targets[0]
    #             original_name = var_name_node.id
                
    #             # **THE FIX**: Removed the restrictive `.isupper()` check.
    #             # Now it renames any variable being assigned a constant value.
    #             if original_name not in self.name_map:
    #                 new_name = var_con_cak()
    #                 self.name_map[original_name] = new_name
                
    #             var_name_node.id = self.name_map[original_name]

    #     self.generic_visit(node)
    #     return node
    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name_node = node.targets[0]
            original_name = var_name_node.id

            if original_name not in self.name_map:
                new_name = var_con_cak()
                self.name_map[original_name] = new_name

            var_name_node.id = self.name_map[original_name]

        self.generic_visit(node)
        return node

    def visit_Name(self, node: ast.Name) -> ast.Name:
        """Updates all usages of a renamed class or constant variable."""
        if node.id in self.name_map:
            node.id = self.name_map[node.id]
        return node


BUILTIN_METHODS = set(dir(type('dummy', (), {})))

class FunctionRenamer(ast.NodeTransformer):
    def __init__(self):
        self.class_map = {}          # old class name -> new name
        self.method_map = {}         # old method name -> new name
        self.class_methods = {}      # class name -> set of its methods

    def visit_ClassDef(self, node: ast.ClassDef):
        original_class_name = node.name
        new_class_name = var_con_cak()
        self.class_map[original_class_name] = new_class_name
        node.name = new_class_name
        self.class_methods[new_class_name] = set()

        for item in node.body:
            if isinstance(item, ast.FunctionDef) and not item.name.startswith("__"):
                new_name = var_con_cak()
                self.method_map[item.name] = new_name
                self.class_methods[new_class_name].add(new_name)
                item.name = new_name
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if not node.name.startswith("__"):
            new_name = var_con_cak()
            self.method_map[node.name] = new_name
            node.name = new_name
        self.generic_visit(node)
        return node

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            if node.id in self.method_map:
                node.id = self.method_map[node.id]
            elif node.id in self.class_map:
                node.id = self.class_map[node.id]
        return node

    def visit_Attribute(self, node: ast.Attribute):
        self.generic_visit(node)
        # Only rename attributes if they belong to a user-defined class
        if node.attr in self.method_map and node.attr not in BUILTIN_METHODS:
            node.attr = self.method_map[node.attr]
        return node


def renamethings(source_code: str) -> ast.Module:
    """
    Parses source code, renames functions, and returns the modified code.
    """
    tree = ast.parse(source_code)
    # transformer = FunctionRenamer()
    transformer1 = ObfuscatorV2()
    # new_tree = transformer.visit(transformer1.visit(tree))
    new_tree = transformer1.visit(tree)
    ast.fix_missing_locations(new_tree)
    return new_tree
if __name__ == "__main__":
    source = """
api_key = "SECRET_STRING_123" 
VALID_IDS = [10, 20, 30]

class OldClassName:
    def __init__(self):
        self.key = api_key

def get_data():
    client = OldClassName()
    print(f"Using key: {client.key}")
    return VALID_IDS

get_data()
    """

    new_code = renamethings(source)
    print("--- Original Code ---")
    print(source)
    print("\n--- Obfuscated Code ---")
    print(ast.unparse(new_code))