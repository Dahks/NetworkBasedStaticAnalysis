import ast

class Parser():
    tree: ast.Module | None = None

    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.tree = ast.parse(file.read())

    def get_function_definitions(self):
        return [fd for fd in ast.walk(self.tree) if isinstance(fd, ast.FunctionDef)]

    def get_function_calls(self):
        """
        Returns: { caller_name: [called_function_names] }
        """
        results = {}

        # 1. Find every function definition in the file
        all_funcs = [node for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef)]

        for func_node in all_funcs:
            calls = []

            # 2. Create a stack to walk through THIS function's body only.
            # We start with the nodes inside the function body.
            stack = [node for node in ast.iter_child_nodes(func_node)]

            while stack:
                curr = stack.pop()

                # If we find a call, extract the name
                if isinstance(curr, ast.Call):
                    calls.append(self._extract_name(curr))

                # CRITICAL: If we hit a nested function definition, STOP.
                # We do not add its children to the stack. This prevents
                # 'inner_func' calls from appearing in 'outer_func's list.
                if isinstance(curr, ast.FunctionDef):
                    continue

                # Add children to the stack to keep searching
                for child in ast.iter_child_nodes(curr):
                    stack.append(child)

            results[func_node.name] = calls

        return results

    def _extract_name(self, node: ast.Call):
        """Helper to get the name from a Call node (handles func() and obj.method())."""
        func = node.func
        if isinstance(func, ast.Name):
            return func.id
        elif isinstance(func, ast.Attribute):
            return func.attr
        return "unknown"

# --- Usage ---
if __name__ == "__main__":
    # Create dummy file
    with open("test.py", "w") as f:
        f.write("""
def my_func():
    print("Hello")
    data.append(1)

def outer():
    def inner():
        nested_call()
    inner()
""")

    parser = Parser("test.py")
    print(parser.get_function_calls())
