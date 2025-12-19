from diffeq.utils.vectors import *

@vector_function
def foo(x, y):
    return vector(
        x=10*y*x + y,
        y=x,
    )

v = vector(x = 10, y = 11)
print('value of input vector: ', v, sep = '\n')
print('function form: ', sep = '\n')
print(foo)
print('function output: ', sep = '\n')
print(foo(v))
print("function's yacobian: ", sep = '\n')
print(foo.yacobian)
print("function's yacobian value: ", sep = '\n')
print(foo.yacobian(v))