import ast

class Parser():
    tree: ast.Module | None = None

    def __init__(self, filename):
        """
        @param filename: entry point of module to inspect

        @raises FileNotExists if filename is not a valid file
        """
        with open(filename, 'r') as file:
            self.tree = ast.parse(file.read())

    def get_function_definitions(self):
        return [fd for fd in ast.walk(self.tree) if isinstance(fd, ast.FunctionDef)]
