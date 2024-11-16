import ast
import logging
from collections import defaultdict

from src.parser.data_classes import Definition, Class


class AstWalker(ast.NodeVisitor):
    """
    Class to walk through an Abstract Syntax Tree (AST) and extract function, method,
    and class definitions along with calls.
    """
    def reset(self):
        # Initialize attributes used to store visited node information
        self.definitions = {}
        self.calls = defaultdict(list)
        self.imports = {}
        self.class_stack = []
        self.module_name = None

    def walk(self, tree: ast.AST, module_name: str) -> [dict, defaultdict]:
        """
        Entry point to extract definitions and calls from an AST.
        """
        self.reset()
        self.module_name = module_name

        self.visit(tree)
        self._resolve_imports_in_calls()
        self._resolve_classes_in_definitions()
        logging.debug(f'Extracted definitions and calls for module: {module_name}')
        return self.definitions, self.calls, self.imports

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Handle class definition nodes.
        """
        class_name = node.name
        logging.debug(f"Found class definition: {class_name}")
        self.class_stack.append(class_name)
        self.definitions[class_name] = Definition(
            name=node.name,
            type="class",
            module=self.module_name,
            start_line=node.lineno,
            end_line=getattr(node, 'end_lineno', None),
        )

        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Handle function or method definition nodes.
        """
        if self.class_stack:
            # Method within a class
            class_name = self.class_stack[-1]
            func_type = 'method'
            func_name = f"{self.module_name}.{class_name}.{node.name}"
        else:
            # Top-level function
            class_name = None
            func_type = 'function'
            func_name = f"{self.module_name}.{node.name}"

        self.definitions[func_name] = Definition(
            name=node.name,
            type=func_type,
            module=self.module_name,
            class_name= class_name,
            start_line=node.lineno,
            end_line=getattr(node, 'end_lineno', None),
        )
        logging.debug(f"Found function definition: {func_name}")
        self._extract_calls_from_function(node, func_name)
        self.generic_visit(node)

    def _extract_calls_from_function(self, node: ast.FunctionDef, func_name: str):
        """
        Extract all function or method calls from a function or method body.
        """
        for child_node in ast.walk(node):
            if isinstance(child_node, ast.Call):
                if isinstance(child_node.func, ast.Name):  # Simple call
                    self.calls[func_name].append(child_node.func.id)
                elif isinstance(child_node.func, ast.Attribute):  # Object.method()
                    self.calls[func_name].append(child_node.func.attr)

    def visit_Import(self, node: ast.Import):
        """
        Handle import statements.
        """
        for alias in node.names:
            self.imports[alias.asname or alias.name] = alias.name
        logging.debug(f"Found import: {self.imports}")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """
        Handle from-import statements.
        """
        module = node.module
        for alias in node.names:
            name = alias.asname or alias.name
            full_name = f"{module}.{alias.name}" if module else alias.name
            self.imports[name] = full_name
        logging.debug(f"Found import from: {self.imports}")

    def _resolve_imports_in_calls(self):
        """
        Resolve function and method calls based on imports and classify all calls.
        """
        logging.debug(f'Resolving calls for module {self.module_name}')
        resolved_calls = defaultdict(list)
        for caller, callees in self.calls.items():
            for callee in callees:
                if callee in self.imports:
                    # Function is defined in another module
                    callee_full_name = self.imports[callee]
                else:
                    # Function is defined in the current module
                    callee_full_name = f'{self.module_name}.{callee}'
                resolved_calls[caller].append(callee_full_name)
        self.calls = resolved_calls
        logging.debug(f'Finished resolving calls for module {self.module_name}')

    def _resolve_classes_in_definitions(self):
        #Todo: fix in a different way -> Should be read in the correct format upon read..
        definitions = self.definitions
        classes = {node.name: node for node in definitions.values() if node.type == 'class'}
        methods = [node for node in definitions.values() if node.type == 'method']

        resolved_classes = {}
        for class_name, definition in classes.items():
            module = definition.module
            methods_of_class = [method for method in methods if method.class_name == class_name]
            resolved_classes[class_name] = Class(name=class_name, module=module, methods=methods_of_class)

        # Clean defintions
        other_defintions = {k: v for k,v in definitions.items() if v.type not in ['method', 'class']}
        resolved_definitions = {**other_defintions, **resolved_classes}
        self.definitions = resolved_definitions
