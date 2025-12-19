## Utils

### symbolic
implements operations with symbols
```python
from diffeq.utils.symbolic import *
x, y = variable('x'), variable('y')
expression = x**2 + y*x + cos(x) + 3

print(expression)

print('without optimizations:')
print(expression.diff('x'))
print(expression.diff('y'))
print('with optimizations:')

print(expression.diff('x').optim())
print(expression.diff('y').optim())

print('second derivative:')
print(expression.diff('x').diff('x').optim())


print('packaging into "programs"')

prog = program({'output':expression})
prog(x = 1, y = 2)


print('execution order:')
print(prog)
```

Output:
```
((x^2)+y*x+cos(x)+3)
without optimizations:
(2*(x^1)*1.0+(0.0*x+y*1.0)+(-sin(x))*1.0+0.0)
(2*(x^1)*0.0+(1.0*x+y*0.0)+(-sin(x))*0.0+0.0)
with optimizations:
(x*2+y+sin(x)*-1)
x
second derivative:
((1^2)*(x^0)*2+cos(x)*-1)
packaging into "programs"
execution order:
x,y,3
(x^2),y*x,cos(x)
((x^2)+y*x+cos(x)+3)
```

### vectors

#### basic operations
inherits from `dict`
```python
# inherits from dict
class vector(dict):...
```

Keys - axis names  
Values - projection values of the vector on the corresponding axis  

When adding/scalar multiplying/element-wise operations, corresponding keys will be added, and in case of mismatched keys, it will be assumed that missing keys have a value of zero.

Example:
``` python
    from diffeq.utils.vectors import *
    A = vector(x = 10, y = 10)      
    B = vector(x = 3, y = -1, z = 1)
>>> print('A:', A, sep = '\n'*2)
A:

┌─────────────┐
│axis │value  │
├─────┼───────┤
│x    │10     │
│y    │10     │
└─────────────┘
>>> print('B:', B, sep = '\n'*2)        
B:

┌─────────────┐
│axis │value  │
├─────┼───────┤
│x    │3      │
│y    │-1     │
│z    │1      │
└─────────────┘
>>> print('A + B:', A + B, sep = '\n'*2)
A + B:

┌──────────────┐
│axis │value   │
├─────┼────────┤
│x    │13      │
│z    │1.0     │
│y    │9       │
└──────────────┘
>>> print('A - B:', A - B, sep = '\n'*2)
A - B:

┌───────────────┐
│axis │value    │
├─────┼─────────┤
│x    │7        │
│z    │-1.0     │
│y    │11       │
└───────────────┘
>>> print('A @ B:', A @ B, sep = '\n'*2)
A @ B:

20
>>> print('A * B:', A * B, sep = '\n'*2)
A * B:

┌──────────────┐
│axis │value   │
├─────┼────────┤
│x    │30      │
│z    │0.0     │
│y    │-10     │
└──────────────┘
>>> print('A / B:', A / B, sep = '\n'*2)
A / B:

┌─────────────────────────────┐
│axis │value                  │
├─────┼───────────────────────┤
│x    │3.3333333333333335     │
│z    │0.0                    │
│y    │-10.0                  │
└─────────────────────────────┘
>>> print('A ** B:', A ** B, sep = '\n'*2)
A ** B:

┌───────────────┐
│axis │value    │
├─────┼─────────┤
│x    │1000     │
│z    │0.0      │
│y    │0.1      │
└───────────────┘
>>> print('A**2:', A**2, sep = '\n'*2)
A**2:

┌──────────────┐
│axis │value   │
├─────┼────────┤
│x    │100     │
│y    │100     │
└──────────────┘
>>> print('2**A:', 2**A, sep = '\n'*2)
2**A:

┌───────────────┐
│axis │value    │
├─────┼─────────┤
│x    │1024     │
│y    │1024     │
└───────────────┘
>>> print('A@A:', A@A)
A@A: 200
```

#### vector functions
Implements methods for working with vector functions. Inherits from `program` in symbolic.
```python
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
print("function's Jacobian: ", sep = '\n')
print(foo.yacobian)
print("function's Jacobian value: ", sep = '\n')
print(foo.yacobian(v))
```

Output:
```
value of input vector: 
┌─────────────┐
│axis │value  │
├─────┼───────┤
│x    │10     │
│y    │11     │
└─────────────┘
function form: 
┌────────────────────────┐
│axis │function          │
├─────┼──────────────────┤
│x    │(y*x*10+y)        │
│y    │x                 │
└────────────────────────┘
function output: 
┌───────────────┐
│axis │value    │
├─────┼─────────┤
│x    │1111     │
│y    │10       │
└───────────────┘
function's Jacobian: 
┌────────────────────────────┐
│axis     │function          │
├─────────┼──────────────────┤
│dx_dx    │(y*10)            │
│dx_dy    │(x*10+1.0)        │
│dy_dx    │1.0               │
│dy_dy    │0.0               │
└────────────────────────────┘
function's Jacobian value: 
┌────────────────────┐
│axis     │value     │
├─────────┼──────────┤
│dx_dx    │110       │
│dx_dy    │101.0     │
│dy_dx    │1.0       │
│dy_dy    │0.0       │
└────────────────────┘
```

--- 
Composition:
```python
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
```

```python
>>> print(composed)
┌─────────────────────────────────────────┐
│axis │function                           │
├─────┼───────────────────────────────────┤
│x    │(((-x)+-1)*3+(-(y*x*10+y)))        │
│y    │(y*x*10+y+-1j)                     │
└─────────────────────────────────────────┘
>>> print(composed(A))
┌──────────────────┐
│axis │value       │
├─────┼────────────┤
│x    │-28         │
│y    │(22-1j)     │
└──────────────────┘
>>> print(foo2(foo1(A)))
┌──────────────────┐
│axis │value       │
├─────┼────────────┤
│x    │-28         │
│y    │(22-1j)     │
└──────────────────┘
>>>
>>> print(composed.yacobian)
┌───────────────────────────────────┐
│axis     │function                 │
├─────────┼─────────────────────────┤
│dx_dy    │((-(x*10+1.0))+3)        │
│dx_dx    │((-y*10)+-3.0)           │
│dy_dy    │(x*10+1.0)               │
│dy_dx    │(y*10)                   │
└───────────────────────────────────┘
>>> print(composed.div)
┌───────────────────────────────────┐
│axis   │function                   │
├───────┼───────────────────────────┤
│div    │(x*10+(-y*10)+-2.0)        │
└───────────────────────────────────┘
>>> print(composed.div.yacobian)
┌───────────────────────┐
│axis       │function   │
├───────────┼───────────┤
│ddiv_dy    │-10        │
│ddiv_dx    │10         │
└───────────────────────┘
```
## plotting

interactive.py
provides the ability to generate an interactive HTML containing one or more trajectories.  
It allows setting the color and display style.
```python
def generate_html(trajectores:list[vector], axes:tuple[str], path = 'output.html', color:callable = __basic_grad, title:str = ''):...
```
---

### Example

```python
from random import gauss, random
import diffeq.plotting.interactive as interactive
from diffeq import *

# Lorenz Attractor
a, b, c = -15, 35, -3/2
solver = rk4_integrator(0.01, 1)
lorenz_sys = system(
    vector_function(lambda x, y, z:vector(x = a*(x - y), y = b*x - y - z*x, z = x*y + c*z)), solver
    )

# calculating trajectories
lorenz_trjs = []
for _ in range(10):
    lorenz_sys.state = vector(x = gauss(), y = gauss(), z = gauss())
    results = lorenz_sys.run(10)
    lorenz_trjs.append(results)

# saving
out = interactive.generate_html(lorenz_trjs, ('x', 'y', 'z'), color = interactive.start_end_grad(), title = 'Lorenz Attractor', path = 'output/lorenz.html')
```
[Output:](output/lorenz.html)

![alt text](images/lorenz.png)



display styles look like this (but the difference is usually not noticeable for long trajectories):
```python
# fading tail
def basic_grad(color = None, transparent_coof = 1.0):
    Col = color
    bias = randint(0, 100)
    def f(t, i, **kwrgs):
        if Col is None:
            color = random_color(i)
        else:
            color = Col
        return color + [t*transparent_coof]
    return f

# fading tail and head
def start_end_grad(color = None, transparent_coof = 1.0):
    Col = color
    bias = randint(0, 100)
    def f(t, i, **kwrgs):
        if Col is None:
            color = random_color(i + bias)
        else:
            color = Col
        return color + [4*t*(1 - t)*transparent_coof]
    return f
```

## diffeq

### integrators
abstract class for numerical integration:
```python 
class integrator: ...
```
Implemented integrators:
```python 
class euler_integrator(integrator): ...
class rk4_integrator(integrator):...
```
By default, integrators when called 
```python
solver.integrate(x, dx)
```
will perform `int(1/dt)` per call.

### system
system is responsible for the integration pipeline
```python
class system:
    def __init__(self, ds_dt: _ve.vector_function, solver, initials: _ve.vector = None):...
```
### Example
```python
from diffeq.utils.vectors import vector, vector_function
from diffeq import system, rk4_integrator

@vector_function
def vector_field(x, y):
    return vector({
        'x': x**2 - y,      # x-component
        'y': x - y**2       # y-component
    })

solver = rk4_integrator(0.01)
sys = system(vector_field, solver, initials=vector(x=1, y=2))
results = sys.run(5)

>>> print(results)
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│axis    │value                                                                                      │
├────────┼───────────────────────────────────────────────────────────────────────────────────────────┤
│x       │[1, -0.6894983901924571, -1.3577716526112518, -1.410813685844128, -1.4140123825971138]     │
│y       │[2, 2.0, 2.0, 2.0, 2.0]                                                                    │
│time    │[0, 1.0, 2.0, 3.0, 4.0]                                                                    │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
```