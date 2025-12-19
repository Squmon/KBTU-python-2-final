## Utils

### symbolic
реализует операции с символами
```python
from diffeq.utils.symbolic import *
x, y = variable('x'), variable('y')
expression = x**2 + y*x + cos(x) + 3

print(expression)

print('без оптимизаций:')
print(expression.diff('x'))
print(expression.diff('y'))
print('с оптимизациями:')

print(expression.diff('x').optim())
print(expression.diff('y').optim())

print('дважды производная:')
print(expression.diff('x').diff('x').optim())


print('упаковка в "программы"')

prog = program({'output':expression})
prog(x = 1, y = 2)


print('порядок выполнения:')
print(prog)
```

Output:
```
((x^2)+y*x+cos(x)+3)
без оптимизаций:
(2*(x^1)*1.0+(0.0*x+y*1.0)+(-sin(x))*1.0+0.0)
(2*(x^1)*0.0+(1.0*x+y*0.0)+(-sin(x))*0.0+0.0)
с оптимизациями:
(x*2+y+sin(x)*-1)
x
дважды производная:
((1^2)*(x^0)*2+cos(x)*-1)
упаковка в "программы"
порядок выполнения:
x,y,3
(x^2),y*x,cos(x)
((x^2)+y*x+cos(x)+3)
```

### vectors

#### basic operations
наследуется от `dict`
```python
# наследник dict
class vector(dict):...
```

Ключи - название оси
Значение - значение проекции вектора на соответствующую ось

При сложении/скалярном произведении/поэлентных операциях соответствующие ключи будут складыватся, а при несовпадении ключей будет предполагатся что отсутствующие ключи имеют значение ноль

Пример:
``` python
>>> from diffeq.utils.vectors import *
>>> A = vector(x = 10, y = 10)      
>>> B = vector(x = 3, y = -1, z = 1)
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
Реализуют методы для работы с векторными функциями. Наследуются от `program` из symbolic
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
print("function's yacobian: ", sep = '\n')
print(foo.yacobian)
print("function's yacobian value: ", sep = '\n')
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
function's yacobian: 
┌────────────────────────────┐
│axis     │function          │
├─────────┼──────────────────┤
│dx_dx    │(y*10)            │
│dx_dy    │(x*10+1.0)        │
│dy_dx    │1.0               │
│dy_dy    │0.0               │
└────────────────────────────┘
function's yacobian value: 
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
предоставляет сгенерировать интерактивный html содержащий в себе одну или более траекторий.
Если возможность задавать цвет и стиль отображения
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

# просчет траекторий
lorenz_trjs = []
for _ in range(10):
    lorenz_sys.state = vector(x = gauss(), y = gauss(), z = gauss())
    results = lorenz_sys.run(10)
    lorenz_trjs.append(results)

# сохранение
out = interactive.generate_html(lorenz_trjs, ('x', 'y', 'z'), color = interactive.start_end_grad(), title = 'Lorenz Attractor', path = 'output/lorenz.html')
```
[Output:](output/lorenz.html)

![alt text](images/lorenz.png)



стили отображения выглядят так (но разницы, как правило не заметно при длинных траекториях):
```python
# затухающий хвост
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

# затухающий хвост и глова
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
Реализованные интеграторы:
```python 
class euler_integrator(integrator): ...
class rk4_integrator(integrator):...
```
по умолчанию интеграторы при вызове 
```python
solver.integrate(x, dx)
```
будут делать `int(1/dt)` за вызов.

### system
system отвечает за pipeline интегрирования
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