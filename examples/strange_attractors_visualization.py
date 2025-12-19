from random import gauss, random
import diffeq.plotting.interactive as interactive
from diffeq import *
import diffeq.utils.symbolic as symb

import os
if not os.path.exists('output'):
    os.makedirs('output')

solver = rk4_integrator(0.01, 1)

# Lorenz Attractor
a, b, c = -15, 35, -3/2
lorenz_sys = system(
    vector_function(lambda x, y, z: vector(
        x=a*(x - y),
        y=b*x - y - z*x,
        z=x*y + c*z)
        ), solver
)
lorenz_trjs = []
for _ in range(10):
    lorenz_sys.state = vector(x=gauss(), y=gauss(), z=gauss())
    results = lorenz_sys.run(10)
    lorenz_trjs.append(results)
out = interactive.generate_html(lorenz_trjs, ('x', 'y', 'z'), color=interactive.start_end_grad(
), title='Lorenz Attractor', path='output/lorenz.html')


# Rössler Attractor
a, b, c = 0.2, 0.2, 7.7
rossler_sys = system(
    vector_function(lambda x, y, z: vector(
        x=-y - z,
        y=x + a*y,
        z=b + z*(x - c))
        ), solver
)
rossler_trjs = []
for _ in range(10):
    rossler_sys.state = vector(x=gauss(), y=gauss(), z=gauss())*3
    results = rossler_sys.run(10)
    rossler_trjs.append(results)
out = interactive.generate_html(rossler_trjs, ('x', 'y', 'z'), color=interactive.start_end_grad(
), title='Rossler Attractor', path='output/rossler.html')


# Lu Chen Attractor
a, b, c, u = 36, 3, 20, -3
multiscroll_sys = system(
    vector_function(lambda x, y, z: vector(
        x=a*(y - x),
        y=x - x*z + c*y + u,
        z=x*y-b*z)
        ), solver
)
multiscroll_trjs = []
for _ in range(10):
    multiscroll_sys.state = vector(
        x=gauss(), y=gauss(), z=gauss()) + vector(x=0.1, y=0.3, z=-0.6)
    results = multiscroll_sys.run(10)
    multiscroll_trjs.append(results)
out = interactive.generate_html(multiscroll_trjs, ('x', 'y', 'z'), color=interactive.start_end_grad(
), title='Lu Chen Attractor', path='output/Lu Chen.html')


# Trillium Attractor
a, b, c, d = 0.1, 0.1, 14, 0.08
trillium_sys = system(
    vector_function(lambda x, y, z: 10*vector(x=a*x - b*y *z,
                                              y=-c*y + x*z,
                                              z=-d*z + x*y
                                              )), solver
)
trillium_trjs = []
for _ in range(50):
    trillium_sys.state = vector(x=gauss(), y=gauss(), z=gauss())*2
    results = trillium_sys.run(10)
    trillium_trjs.append(results)
out = interactive.generate_html(trillium_trjs, ('x', 'y', 'z'), color=interactive.start_end_grad(
), title='Trillium Attractor', path='output/trillium.html')


# Tomas Attractor
a, b = 0.2, 1.0
tomas_sys = system(
    vector_function(lambda x, y, z: vector(
        x=-a*x + b*symb.sin(y),
        y=-a*y + b*symb.sin(z),
        z=-a*z + b*symb.sin(x))
        ), solver
)
tomas_trjs = []
for _ in range(10):
    tomas_sys.state = 5*(vector(x=random(), y=random(), z=random())*2 - 1.0)
    results = tomas_sys.run(100)
    tomas_trjs.append(results)
out = interactive.generate_html(tomas_trjs, ('x', 'y', 'z'), color=interactive.start_end_grad(
), title='Tomas Attractor', path='output/tomas.html')


# linear system
linear_sys = system(
    vector_function(lambda x, y, z: vector(
        x=-y,
        y=x,
        z=-0.3*z
        )), solver
)
linear_trjs = []
for _ in range(50):
    linear_sys.state = vector(x=gauss(), y=gauss(), z=gauss())*2
    results = linear_sys.run(10)
    linear_trjs.append(results)
out = interactive.generate_html(linear_trjs, ('x', 'y', 'z'), color=interactive.start_end_grad(
), title='linear system', path='output/linear.html')
