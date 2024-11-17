import logging

from src.poseidon import poseidon

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Example 1
poseidon(
    folder_path="examples/example_with_modules",
    graph_type='call',
    output_path='output/example_with_modules.jpg'
)

# Example 2
poseidon(
    folder_path="examples/example_with_classes",
    graph_type='call',
    output_path='output/example_with_classes.png'
)

# Example 3
poseidon(
    folder_path="examples/example_ignore",
    graph_type='call',
    output_path='output/example_ignore_show_all.png'
)


# Example 4
poseidon(
    folder_path="examples/example_ignore",
    graph_type='call',
    output_path='output/example_show_private.png',
    exclude_private=False,
)

poseidon(
    folder_path="examples/example_ignore",
    graph_type='call',
    output_path='output/example_show_external.png',
    exclude_external=False,
)