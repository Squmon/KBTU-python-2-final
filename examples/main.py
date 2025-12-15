from diffeq import *
from diffeq.utils.vectors import *

A = vector_function(vector(
    x = lambda x, y: x,
    y = lambda x, y: y + x,
), ('x', 'y'))

B = vector_function(vector(
    x = lambda x, y: y,
    y = lambda x, y: x + y,
), ('x', 'y'))

C = vector_function(lambda **args:B((args)), ('x', 'y'), ('x', 'y'))

S = system(vector_function(
    vector(
        x = lambda x, y: -y,
        y = lambda x, y: x
    ), ('x', 'y')
), rk4_integrator(0.01))

print(C(vector(x = 3, y = 2)))

print(len(S.run(10)['s']['x']))