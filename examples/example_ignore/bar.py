"""
The private and protected function both call a public one. When ignoring the private functions, we want a yellow edge
indicating that the public one is being called.


"""
import numpy as np

from .foo import foo

class Dog:
    def fun_with_external_call(self):
        array = np.array([2, 3])
        sum = np.sum(array)
        np.testing.assert_allclose(sum, 5)
        return sum

    def fun_with_std_call(self):
        print('hoi')

    def public(self):
        self.__private()
        self._protected()

    def __private(self):
        compute_sum()

    def _protected(self):
        compute_sum()

    def foo(self):
        foo()


def compute_sum(a, b):
    return a + b