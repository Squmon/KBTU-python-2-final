from diffeq.SDE import *
from diffeq.utils.vectors import *

A = VectorFunction(Vector(
    x = lambda x, y: x,
    y = lambda x, y: y + x,
), ('x', 'y'))

B = VectorFunction(Vector(
    x = lambda x, y: y,
    y = lambda x, y: x + y,
), ('x', 'y'))

C = VectorFunction(lambda **args:B((args)), ('x', 'y'), ('x', 'y'))

S = system(VectorFunction(
    Vector(
        x = lambda x, y: -y,
        y = lambda x, y: x
    ), ('x', 'y')
), rk4_integrator(0.01))

print(C(Vector(x = 3, y = 2)))

print(len(S.run(10)['s']['x']))