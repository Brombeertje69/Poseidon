import argparse
import logging

from src.parser import Parser
from src.graphs import CallGraph

def poseidon(
        folder_path: str,
        graph_type: str = 'call',
        title: str = None,
        output_path: str = 'graph.png',
        exclude_private: bool = True,
        exclude_external: bool = True
    ):
    """ The high-level function that combines the parser with the graphs

    Args:
        folder_path: The path of the source code to be parsed
        graph_type: The graph type to be produced
        title: Title of the graph to be produced
        output_path: The path where the graph should be stored
        exclude_private: Option to exclude private functions from the graph
        exclude_external: Option to exclude external calls from the graph
    """
    # Setup the parser
    parser = Parser(
        exclude_private=exclude_private,
        exclude_external=exclude_external
    )
    modules = parser.parse_folder(folder_path=folder_path)

    if graph_type == 'call':
        graph = CallGraph(output_path=output_path, title=title)
        graph.build_graph(modules)
        graph.render()


# Define CLI
def main():
    # Create the ArgumentParser object
    parser = argparse.ArgumentParser(description="My awesome CLI tool")

    # Add arguments to the parser
    parser.add_argument('folder', type=str, help="Folder to be inspected")
    parser.add_argument('-o', type=str, default="graph.png", help="Location of output file")
    parser.add_argument('-g', '--graph-type', type=str, choices=['call', 'sequence', 'class'],
                        default='call', help="Type of graph to generate (call, sequence, class)")
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Increase verbosity of output (-v for INFO, -vv for DEBUG)")
    parser.add_argument('-t', '--title',  type=str, default=None,  help="Title of the graph")
    # Exclude options
    parser.add_argument('--exclude-private', type=bool, default=True,
                        help="Exclude private methods and attributes (default: True)")
    parser.add_argument('--exclude-external', type=bool, default=True,
                        help="Exclude external calls outside the inspected folder (default: True)")

    # Parse the arguments
    args = parser.parse_args()

    # Set the logging level based on the verbosity (-v and -vv)
    if args.verbose == 1:
        log_lvl = logging.INFO
    elif args.verbose >= 2:
        log_lvl = logging.DEBUG
    else:
        log_lvl = logging.WARNING
    logging.basicConfig(level=log_lvl, format='%(asctime)s - %(levelname)s - %(message)s')

    # Call the poseidon function with the parsed arguments
    poseidon(**vars(args))


if __name__ == "__main__":
    main()