from typing import Callable
import symbolic as symb


class vector(dict):
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


class vector_function(symb.program):
    def __init__(self, function: vector[str:Callable] | Callable, input_signature: tuple | set[str], output_signature: tuple | set[str] = None):
        self.in_axes: set = set(input_signature)
        self.out_axes = tuple(function.keys()) if output_signature is None else output_signature
        self.__vars: dict['str':symb.variable] = {
            k: symb.variable(k) for k in input_signature}
        self.foo = function(**self.__vars) if callable(function) else {k: function[k](**self.__vars) for k in self.out_axes}
        print(self.foo)
        super().__init__(self.foo)
        self.__yacobian = None

    def __call__(self, vec: dict | vector):
        return vector(super().__call__(**vec))

    def yacobian(self, vec: dict | vector):
        if self.__yacobian is not None:
            return self.__yacobian(**vec)
        F = dict()
        for outa in self.out_axes:
            for ina in self.in_axes:
                inds = outa + '_' + ina
                F[inds] = self.c[outa].diff(ina)

        self.__yacobian = symb.program(F)
        return self.yacobian(vec)

    def yacobian_prog(self):
        return self.__yacobian