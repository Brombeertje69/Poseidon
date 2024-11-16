from src.parser import Parser
from src.graphs import CallGraph

import logging

# Configure logging
logging.basicConfig(level=logging.info, format='%(asctime)s - %(levelname)s - %(message)s')

# Example 1
# folder_path = "examples/example_with_modules"  # Replace with the path to your folder
# parser = Parser()
# modules = parser.parse_folder(folder_path=folder_path)
# graph = CallGraph()
# graph.build_graph(modules)
# graph.render(output_path='output/example_with_modules.jpg')


# Example 2
folder_path = "examples/example_with_classes"  # Replace with the path to your folder
parser = Parser()
modules = parser.parse_folder(folder_path=folder_path)
graph = CallGraph()
graph.build_graph(modules)
graph.render(output_path='output/example_with_classes.png')