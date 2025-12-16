from diffeq import *
from diffeq.utils.vectors import *


@vector_function
def foo(x, y):
    return vector(
        x = 10*y*x + y,
        y = -x + (-1),
    )

S = system(foo, rk4_integrator(0.01))
print(len(S.run(10)['s']['x']))
print(foo)
print(foo.show_yacobian())
print(foo.yacobian(vector(
    x = 1,
    y = 2
)))

print(vector(
    x = 10,
    y = 100
))