import graphviz
import logging
import os

from src.parser import Class, Definition

class CallGraph:
    def __init__(self):
        """Initialize the call graph."""
        self.graph = graphviz.Digraph(engine='dot')
        self.graph.attr(dpi='300')  # High-quality output

    def build_graph(self, modules):
        """Build the call graph based on the parsed modules."""
        logging.info(f"Building graph with {len(modules)} modules.")
        for module_name, module in modules.items():
            logging.debug(f"Processing module: {module_name}")
            # Create a subgraph for the module that groups all functions and calls inside a dotted box
            with self.graph.subgraph(name=f"cluster_{module_name}") as subgraph:
                subgraph.attr(label=module_name, style='dotted', color='black')  # Dotted box for module
                for full_name, definition in module.definitions.items():
                    # Add each function in the module
                    if type(definition) == Definition:
                        self._add_function(graph=subgraph, full_name=full_name, definition=definition)
                        # Detect leaf functions (functions that do not have any calls)
                        if not module.calls[full_name]:
                            self._add_function(graph=subgraph, full_name=full_name, definition=definition, is_leaf=True)
                    elif type(definition) == Class:
                        self._add_class(subgraph, definition=definition)

                # Add calls for each function
                for caller, callees in module.calls.items():
                    for callee in callees:
                        self._add_call(caller, callee)

    def _add_function(self, graph, full_name, definition: Definition, is_leaf=False):
        """Create a function node, marking leaf nodes in green."""
        logging.debug(f"Adding function: {full_name}")
        color = 'green' if is_leaf else 'lightblue'
        graph.node(full_name, label=definition.name, style='filled', fillcolor=color)

    def _add_class(self, graph, definition: Class):
        """Create a box for a graph and add the methods"""
        class_name = definition.name
        module = definition.module
        methods = definition.methods
        with graph.subgraph(name=f"cluster_{module}_{class_name}") as class_graph:
            class_graph.attr(label=f'Class: {class_name}',
                             style='solid', color='black', penwidth='0.7', bgcolor='#f2f2f2' )  # Box for class
            for method_name, method in methods.items():
                full_name = f'{module}.{method.class_name}.{method.name}'
                logging.debug(f'adding method {full_name}')
                self._add_function(class_graph, full_name, definition=method)


    def _add_call(self, caller, callee):
        """Add a directed edge for a function call."""
        logging.debug(f"Adding call from {caller} to {callee}.")
        self.graph.edge(caller, callee)

    def render(self, output_path: str ='call_graph.png', title: str = None):
        """Render the graph to a file."""
        # Extract the file extension to determine the format
        base_name, file_extension = os.path.splitext(output_path)
        file_extension = file_extension.lstrip('.')  # Remove leading dot if present

        # Add title to graph
        if title is None:
            title = base_name.split('/')[-1]
        self._add_title(title=title)

        # If an extension is provided, use it as the format
        if file_extension:
            # Only set the format if it wasn't already set
            self.graph.format = file_extension
            logging.info(f"Graph format set to {file_extension}.")
        else:
            # Default to 'png' if no extension is specified
            self.graph.format = 'png'
            logging.info("No format specified. Defaulting to PNG.")

        # If no extension was specified, append the format to the base name
        if not file_extension:
            output_path = base_name + '.' + self.graph.format

        # Render the graph with the correct output path and format
        self.graph.render(outfile=output_path, cleanup=True)  # This will use the specified output path
        logging.info(f"Graph rendered and saved to {output_path}")

    def _add_title(self, title):
        # Add a title to the graph with customization
        self.graph.attr(
            label=title,
            fontsize='28',
            fontname='Helvetica',
            fontweight='bold',
            labelloc='t'
        )

