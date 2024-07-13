import pytest
from src.mermaid_diagram_generator import MermaidSequenceDiagramGenerator

def test_basic_method_calls():
    source_code = '''
class A:
    def method1(self):
        b = B()
        b.method2()

class B:
    def method2(self):
        pass
'''
    expected_diagram = '''
sequenceDiagram
    A ->> b: method2()
'''
    generator = MermaidSequenceDiagramGenerator(source_code)
    generated_diagram = generator.generate_diagram()
    assert generated_diagram == expected_diagram, f"Expected diagram:\n{expected_diagram}\n\nGenerated diagram:\n{generated_diagram}"

def test_method_calls_with_instance_creation():
    source_code = '''
class A:
    def method1(self):
        b = B()
        b.method2()

class B:
    def method2(self):
        c = C()
        c.method3()

class C:
    def method3(self):
        pass
'''
    expected_diagram = '''
sequenceDiagram
    A ->> b: method2()
    B ->> c: method3()
'''
    generator = MermaidSequenceDiagramGenerator(source_code)
    generated_diagram = generator.generate_diagram()
    assert generated_diagram == expected_diagram, f"Expected diagram:\n{expected_diagram}\n\nGenerated diagram:\n{generated_diagram}"

def test_multiple_method_calls():
    source_code = '''
class A:
    def method1(self):
        b = B()
        b.method2()
        c = C()
        c.method3()

class B:
    def method2(self):
        pass

class C:
    def method3(self):
        pass
'''
    expected_diagram = '''
sequenceDiagram
    A ->> b: method2()
    A ->> c: method3()
'''
    generator = MermaidSequenceDiagramGenerator(source_code)
    generated_diagram = generator.generate_diagram()
    assert generated_diagram == expected_diagram, f"Expected diagram:\n{expected_diagram}\n\nGenerated diagram:\n{generated_diagram}"


def test_self_method_called():
    source_code = '''
class A:
    def method1(self):
        self.method2()
    
    def method2(self):
        pass

'''
    expected_diagram = '''
sequenceDiagram
    A ->> A: method2()
'''
    generator = MermaidSequenceDiagramGenerator(source_code)
    generated_diagram = generator.generate_diagram()
    assert generated_diagram == expected_diagram, f"Expected diagram:\n{expected_diagram}\n\nGenerated diagram:\n{generated_diagram}"