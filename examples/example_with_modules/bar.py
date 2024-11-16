from .foo import foo
from .package1.baz import compute_sum

def bar(a, b):
    c = foo(a, b)
    return c

bar(3, 5)

def bar2():
    return compute_sum(3, 4, 5)