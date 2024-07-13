import ast


class SequenceDiagramParser(ast.NodeVisitor):
    """
    A parser to extract method calls between classes from Python source code.

    This class traverses the abstract syntax tree (AST) of the source code to
    identify and record the method calls made from one class to another.

    Attributes:
        class_stack (list): A stack to keep track of the current class being visited.
        method_stack (list): A stack to keep track of the current method being visited.
        calls (list): A list to store tuples representing the calls between methods of different classes.
                     Each tuple is of the form (caller_class, caller_method, callee_class, callee_method).
    """

    def __init__(self):
        """Initialize the parser with empty stacks and an empty calls list."""
        self.class_stack = []
        self.method_stack = []
        self.calls = []

    def visit_ClassDef(self, node):
        """
        Visit a class definition node and traverse its body.

        Args:
            node (ast.ClassDef): The class definition node to visit.

        This method adds the class name to the class_stack, visits all child nodes,
        and then pops the class name from the stack.
        """
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node):
        """
        Visit a function definition node and traverse its body.

        Args:
            node (ast.FunctionDef): The function definition node to visit.

        This method adds the method name to the method_stack, visits all child nodes,
        and then pops the method name from the stack.
        """
        self.method_stack.append(node.name)
        self.generic_visit(node)
        self.method_stack.pop()

    def visit_Call(self, node):
        """
        Visit a function call node and record the call if it is a method call on an instance.

        Args:
            node (ast.Call): The function call node to visit.

        If the function call is an attribute (method call) on an instance of another class,
        this method records the caller class, caller method, callee class, and callee method
        in the calls list. Then it continues to visit all child nodes.
        """
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            if isinstance(node.func.value, ast.Name):
                class_name = node.func.value.id
                if self.class_stack:
                    caller_class = self.class_stack[-1]
                    caller_method = self.method_stack[-1] if self.method_stack else None
                    self.calls.append((caller_class, caller_method, class_name, method_name))
        self.generic_visit(node)

    def get_calls(self):
        """
        Get the list of calls between methods of different classes.

        Returns:
            list: A list of tuples representing the calls. Each tuple contains
                  (caller_class, caller_method, callee_class, callee_method).
        """
        return self.calls


def parse_source_code(source_code):
    """
    Parse the provided Python source code to extract method calls between classes.

    Args:
        source_code (str): The Python source code to parse.

    Returns:
        list: A list of tuples representing the calls between methods of different classes.
              Each tuple contains (caller_class, caller_method, callee_class, callee_method).
    """
    tree = ast.parse(source_code)
    parser = SequenceDiagramParser()
    parser.visit(tree)
    return parser.get_calls()

if __name__ == '__main__':
    # Example usage
    source_code = '''
    class A:
        def method1(self):
            b = B()
            b.method2()
    
    class B:
        def method2(self):
            pass
    
    class C:
        def method3(self):
            a = A()
            a.method1()
            b = B()
            b.method2()
    '''

    calls = parse_source_code(source_code)
    for call in calls:
        print(f'{call[0]}.{call[1]} calls {call[2]}.{call[3]}')