import os
import ast
import logging

from src.parser.ast_walker import AstWalker
from src.parser.data_classes import Module


class Parser:
    def __init__(self, resolve_imports=True, resolve_classes=True):
        """Initialize the parser with a folder path.

        Args:
            resolve_imports (bool): Option to automatically resolve import in function calls
        """
        self.resolve_imports = resolve_imports
        self.resolve_classes = resolve_classes
        self.ast_walker = AstWalker()  # Create an instance of AstWalker

    def parse_folder(self, folder_path) -> dict[str, Module]:
        """
        Parse all Python files in the folder and store results in `parse_results`.

        Args:
            folder_path (str): The path to the folder containing Python files.
        """
        logging.info(f'Starting to parse folder: {folder_path}')
        modules = {}
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    module_name = os.path.relpath(file_path, folder_path).replace('\\', '.')
                    logging.info(f'Parsing module: {module_name}')
                    modules[module_name] = self.parse_file(file_path, module_name)
        logging.info('Finished parsing folder')
        return modules

    def parse_file(self, file_path, module_name):
        """
        Parse a single Python file into a `Module`.

        Args:
            file_path (str): The path to the Python file.
            module_name (str): The name of the module (file).

        Returns:
            Module: A `Module` instance containing definitions, calls, and imports.
        """
        module_name = module_name.removesuffix('.py')
        logging.debug(f'Parsing file: {file_path}')
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        try:
            tree = ast.parse(source_code, filename=file_path)
            logging.debug(f'Parsed AST for {file_path}')
        except SyntaxError as e:
            logging.error(f"Syntax error in {file_path}: {e}")
            return Module()

        # Use AstWalker to extract definitions and calls
        definitions, calls, imports = self.ast_walker.walk(tree, module_name)
        logging.debug(f'Finished parsing file: {file_path}')
        return Module(definitions=definitions, calls=calls, imports=imports)

