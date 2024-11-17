import graphviz
import logging
import os

from src.parser import Class, Definition

class CallGraph:
    def __init__(self, output_path: str = 'call_graph.png', title: str = None):
        """Initialize the call graph."""
        # Set attributes
        self.output_path = output_path

        # Extract other attributes based on the output path
        base_name, file_extension = os.path.splitext(self.output_path)
        self.base_name = base_name
        self.file_extension = file_extension.lstrip('.') if file_extension else  '.png'  # Remove leading dot if present
        self.title = base_name.split('/')[-1] if title is None else title

    def build_graph(self, modules):
        """Build the call graph based on the parsed modules."""
        # Create empty graph
        self._init_graph()

        # Process modules
        logging.debug(f"Building graph with {len(modules)} modules.")
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
        self._add_title()

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

    def render(self):
        """Render the graph to a file."""
        # If no extension was specified, append the format to the base name
        output_path = self.output_path if self.file_extension else self.base_name + '.' + self.graph.format

        # Render the graph with the correct output path and format
        self.graph.render(outfile=output_path, cleanup=True)  # This will use the specified output path
        logging.info(f"Graph rendered and saved to {output_path}")

    def _init_graph(self):
        # Create empty graph
        self.graph = graphviz.Digraph(engine='dot')
        self.graph.attr(dpi='300')  # High-quality output
        self._set_format()


    def _set_format(self):
        self.graph.format = self.file_extension
        logging.debug(f"Graph format set to {self.file_extension}.")

    def _add_title(self):
        # Add a title to the graph with customization
        self.graph.attr(
            label=self.title,
            fontsize='28',
            fontname='Helvetica',
            fontweight='bold',
            labelloc='t'
        )
        logging.debug(f"Added title to graph")
