from diffeq.utils.vectors import *

@vector_function
def foo1(x, y):
    return vector(
        x=10*y*x + y,
        y=-x + (-1),
    )

@vector_function
def foo2(x, y):
    return vector(
        x = 3*y - x,
        y = x - 1j
    )

@vector_function
def composed(x, y):
    return foo2(foo1(vector(x = x, y = y)))

A = vector(x = 1, y = 2)
print(composed)
print(composed(A))
print(foo2(foo1(A)))
print(composed.yacobian)
print(composed.div)
print(composed.div.yacobian)