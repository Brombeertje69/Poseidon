import pytest

from src.sequence_diagram_parser import SequenceDiagramParser


# Import the SequenceDiagramParser and parse_source_code function
# from your module if they are defined in another file.
# For example, if they are in a file named `sequence_parser.py`, use:
# from sequence_parser import SequenceDiagramParser, parse_source_code


class TestSequenceDiagramParser:
    def setup_method(self):
        self.parser = SequenceDiagramParser()

    def __test(self, source_code, expected_calls):
        self.parser.parse(source_code)
        calls = self.parser.get_calls()
        assert calls == expected_calls


    def test_single_method_call(self):
        source_code = """
class A:
    def method1(self):
        b = B()
        b.method2()

class B:
    def method2(self):
        pass
"""
        expected_calls = [('A', 'method1', 'b', 'method2')]
        self.__test(source_code=source_code, expected_calls=expected_calls)

    def test_multiple_method_calls(self):
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
        expected_calls = [
            ('A', 'method1', 'b', 'method2'),
            ('A', 'method1', 'c', 'method3')
        ]
        self.__test(source_code=source_code, expected_calls=expected_calls)

    def test_method_calls_in_different_classes(self):
        source_code = '''
class A:
    def method1(self):
        b = B()
        b.method2()

class B:
    def method2(self):
        pass

class C:
    def method3(self):
        a = A()
        a.method1()
        b = B()
        b.method2()
'''
        expected_calls = [
            ('A', 'method1', 'b', 'method2'),
            ('C', 'method3', 'a', 'method1'),
            ('C', 'method3', 'b', 'method2')
        ]
        self.__test(source_code=source_code, expected_calls=expected_calls)

    def test_no_method_calls(self):
        source_code = '''
class A:
    def method1(self):
        pass

class B:
    def method2(self):
        pass
'''
        expected_calls = []
        self.__test(source_code=source_code, expected_calls=expected_calls)

    def test_nested_method_calls(self):
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
        expected_calls = [
            ('A', 'method1', 'b', 'method2'),
            ('B', 'method2', 'c', 'method3')
        ]
        self.__test(source_code=source_code, expected_calls=expected_calls)

    def test_method_calls_on_self(self):
        source_code = '''
class A:
    def method1(self):
        self.method2()

    def method2(self):
        pass
'''
        expected_calls = [('A', 'method1', 'self', 'method2')]
        self.__test(source_code=source_code, expected_calls=expected_calls)
