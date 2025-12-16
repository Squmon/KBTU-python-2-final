from typing import Callable
import diffeq.utils.symbolic as symb
from diffeq.utils.string_operations import get_table

class vector(dict):
    def __str__(self):
        return get_table(('axis', 'value'), [[k, str(v)] for k, v in self.items()])

    def __getitem__(self, key):
        return super().get(key, 0.0)
    
    def apply_vector_operation(self, b, operation):
        total_keys = set(b.keys()) | set(self.keys())
        return vector(
            {k: operation(self.get(k, 0.0), b.get(k, 0.0)) for k in total_keys}
        )

    def apply_scalar_operation(self, scalar, operation):
        return vector(
            {k: operation(v, scalar) for k, v in self.items()}
        )

    def __standart_branch(self, b, operation=None):
        if isinstance(b, vector) or type(b) is dict:
            return self.apply_vector_operation(b, operation)
        else:
            return self.apply_scalar_operation(b, operation)

    def __add__(self, b: dict):
        return self.__standart_branch(b, lambda x, y: x+y)

    def __radd__(self, b: dict):
        return self.__standart_branch(b, lambda x, y: y+x)

    def __sub__(self, b: dict):
        return self.__standart_branch(b, lambda x, y: x-y)

    def __rsub__(self, b: dict):
        return self.__standart_branch(b, lambda x, y: y-x)

    def __pow__(self, b):
        return self.__standart_branch(b, lambda x, y: x**y)

    def __mul__(self, b):
        return self.__standart_branch(b, lambda x, y: x*y)

    def __rmul__(self, b):
        return self.__standart_branch(b, lambda x, y: y*x)

    def __rdiv__(self, b):
        return self.__standart_branch(b, lambda x, y: y/x)

    def __div__(self, b):
        return self.__standart_branch(b, lambda x, y: x/y)

    def __neg__(self):
        return vector(
            {k: -v for k, v in self.items()}
        )

    def __matmul__(self, b):
        total_keys = set(b.keys()) | set(self.keys())
        return sum(b.get(k, 0) * self.get(k, 0) for k in total_keys)

def vector_function_to_str(foo):
    d = foo.c
    return get_table(('axis', 'function'), [[k, str(v)] for k, v in d.items()])


class vector_function(symb.program):
    def __init__(self, function: Callable):
        input_signature = function.__code__.co_varnames
        self.in_axes: set = set(input_signature)
        self.__vars: dict['str':symb.variable] = {
            k: symb.variable(k) for k in input_signature}
        out = function(**self.__vars)
        self.out_axes = out.keys()
        self.__foo = out
        super().__init__(self.__foo)
        self.__yacobian = None

    def __call__(self, vec: dict | vector):
        return vector(super().__call__(**vec))

    def __str__(self):
        return vector_function_to_str(self)

    def __generate_yacobian(self):
        if self.__yacobian is None:
            F = dict()
            for outa in self.out_axes:
                for ina in self.in_axes:
                    inds = 'd' + outa + '_d' + ina
                    F[inds] = self.c[outa].diff(ina)

            self.__yacobian = symb.program(F)

    def yacobian(self, vec: dict | vector):
        self.__generate_yacobian()
        return vector(self.__yacobian(**vec))
    
    def show_yacobian(self):
        self.__generate_yacobian()
        return vector_function_to_str(self.__yacobian)

    def yacobian_prog(self):
        return self.__yacobian