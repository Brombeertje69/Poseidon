from src.sequence_diagram_parser import SequenceDiagramParser


class MermaidSequenceDiagramGenerator:
    """
    Generates a Mermaid sequence diagram from Python source code.

    Attributes:
        source_code (str): The Python source code from which to generate the diagram.
    """

    def __init__(self, source_code):
        """
        Initialize the generator with Python source code.

        Args:
            source_code (str): The Python source code from which to generate the diagram.
        """
        self.source_code = source_code

    def generate_diagram(self) -> str:
        """
        Generate a Mermaid sequence diagram from the source code

        Returns:
            A string representing the Mermaid sequence diagram.
        """
        parser = SequenceDiagramParser()
        parser.parse(self.source_code)
        calls = parser.get_calls()
        diagram_lines = self.__format_diagram_lines(calls)
        diagram = self.__format_mermaid_diagram(diagram_lines)
        return diagram

    def __format_diagram_lines(self, calls: list[tuple]) -> str:
        """
        Format method calls into Mermaid sequence diagram lines.

        Args:
            calls: A list of tuples representing method calls.

        Returns:
            A string representing the formatted method calls as Mermaid sequence diagram lines.
        """
        lines = []
        for caller_class, _, callee_class, callee_method in calls:
            lines.append(f'{caller_class} ->> {callee_class}: {callee_method}()')
        return '\n    '.join(lines)

    def __format_mermaid_diagram(self, diagram_lines: str) -> str:
        """
        Format diagram lines into a complete Mermaid sequence diagram.

        Args:
            diagram_lines: A string representing formatted method call lines.

        Returns:
            A string representing the complete Mermaid sequence diagram.
        """
        return f'''
sequenceDiagram
    {diagram_lines}
'''