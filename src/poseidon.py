import argparse
import logging

from src.parser import Parser
from src.graphs import CallGraph

def poseidon(folder_path, graph_type, output_path):
    # Setup the parser
    parser = Parser()
    modules = parser.parse_folder(folder_path=folder_path)

    if graph_type == 'call':
        graph = CallGraph()
        graph.build_graph(modules)
        graph.render(output_path=output_path)


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
    poseidon(args.folder, args.graph_type, args.o)


if __name__ == "__main__":
    main()