import ast


class SequenceDiagramParser:
    """
    Parses Python source code to extract method calls between classes.

    Attributes:
        source_code: The Python source code to parse.
        calls (list): A list to store extracted method calls as tuples.
                      Each tuple contains (caller_class, caller_method, callee_class, callee_method).
    """

    def __init__(self):
        """
        Initialize the parser with empty call stack
        """
        self.calls = []

    def parse(self, source_code: str):
        """
        Parse the stored Python source code to extract method calls.
        """
        tree = ast.parse(source_code)
        self.visit(tree)

    def visit(self, node):
        """
        Recursively visit each node in the AST to extract method calls.

        Args:
            node (ast.AST): The current node in the AST to visit.
        """
        if isinstance(node, ast.ClassDef):
            self.current_class = node.name
        elif isinstance(node, ast.FunctionDef):
            self.current_method = node.name
        elif isinstance(node, ast.Call):
            caller_class = self.current_class if hasattr(self, 'current_class') else None
            caller_method = self.current_method if hasattr(self, 'current_method') else None
            callee_class = None
            callee_method = None
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                callee_class = node.func.value.id
                callee_method = node.func.attr
            if caller_class and callee_class and callee_method:
                self.calls.append((caller_class, caller_method, callee_class, callee_method))

        for child_node in ast.iter_child_nodes(node):
            self.visit(child_node)

    def get_calls(self):
        """
        Retrieve the parsed method calls.

        Returns:
            list: A list of tuples representing method calls.
                  Each tuple contains (caller_class, caller_method, callee_class, callee_method).
        """
        return self.calls