# Differential Equations Library (diffeq-lib)

A Python library for solving, analyzing, and visualizing differential equations without external dependencies. Developed for KBTU Python II final project.

## Features

- **Numerical Integration**: Euler, Runge-Kutta 4th order methods
- **Symbolic Computation**: Automatic differentiation, Jacobian, divergence
- **Vector Operations**: Custom vector class with mathematical operations
- **Visualization**: Phase portraits, trajectories, vector fields using Turtle
- **Numerical Calculus**: Numerical Jacobian and divergence computation

## Installation

### From Wheel File (Recommended)
The package is already built. Your wheel file is in `dist/diffeq_lib-0.1.0-py3-none-any.whl`.

```bash
pip install dist/diffeq_lib-0.1.0-py3-none-any.whl
```

### From Source
```bash

#cloning the repository
git clone https://github.com/Squmon/KBTU-python-2-final.git
cd KBTU-python-2-final

#installing the package 
pip install .
```

### Verify Installation
```bash

python -c "from diffeq.utils.calculus import jacobian, divergence; print('✅ Your numerical calculus methods are installed!')"
```

## Quick Start
```python

#inporting numerical calculus methods
from diffeq.utils.calculus import jacobian, divergence
from diffeq.utils.vectors import vector

#defining a vector field for analysis
def vector_field(state):
    x, y = state['x'], state['y']
    return vector({
        'x': x**2 - y,      # x-component
        'y': x + y**2       # y-component
    })

#pointing to analyze
point = vector({'x': 2.0, 'y': 3.0})

#usage of numerical methods
J = jacobian(vector_field, point)  # Numerical Jacobian
div = divergence(vector_field, point)  # Numerical divergence

print("Vector field analysis at (2, 3):")
print(f"Jacobian matrix:")
print(f"  [ {J['dx_dx']:.2f}  {J['dx_dy']:.2f} ]")
print(f"  [ {J['dy_dx']:.2f}  {J['dy_dy']:.2f} ]")
print(f"Divergence: {div:.2f}")

#optionally: solving the system (Ilya's part)
from diffeq import system, rk4_integrator

solver = rk4_integrator(0.01)
sys = system(vector_field, solver, initials=vector(x=1, y=1))
results = sys.run(5)

print(f"\nSystem solved! Final state: x={results['x'][-1]:.4f}, y={results['y'][-1]:.4f}")
```

## Numerical Calculus Methods

The library provides numerical computation of Jacobian and divergence using central difference schemes with adaptive step sizing.
jacobian(F, x: vector, h=None) -> vector

Computes the numerical Jacobian matrix of a vector function F at point x.

Parameters:

    F: Callable that takes a vector and returns a vector

    x: Point where to compute Jacobian (vector object)

    h: Step size (optional, auto-adapts if None)

Returns:

    vector with keys formatted as 'd{out}_d{in}' containing partial derivatives

### Example:
```python

from diffeq.utils.calculus import jacobian
from diffeq.utils.vectors import vector

def lorenz_system(state):
    sigma, rho, beta = 10.0, 28.0, 8.0/3.0
    x, y, z = state['x'], state['y'], state['z']
    return vector({
        'x': sigma * (y - x),
        'y': x * (rho - z) - y,
        'z': x * y - beta * z
    })

point = vector({'x': 0.0, 'y': 1.0, 'z': 1.05})
J = jacobian(lorenz_system, point)

print("Jacobian at (0, 1, 1.05):")
print(f"  ∂ẋ/∂x = {J['dx_dx']:.4f}")
print(f"  ∂ẋ/∂y = {J['dx_dy']:.4f}")
print(f"  ∂ẏ/∂z = {J['dy_dz']:.4f}")
```

divergence(F, x: vector, h=None) -> float

Computes the numerical divergence of a vector field F at point x.

Parameters:

    F: Vector field function

    x: Evaluation point

    h: Step size (optional, auto-adapts if None)

Returns:

    Scalar divergence value

Raises:

    ValueError if input and output axes don't match

### Example:
```python

from diffeq.utils.calculus import divergence

def incompressible_flow(state):
    x, y = state['x'], state['y']
    return vector({'x': -y, 'y': x})  # Rotational flow

def compressible_flow(state):
    x, y = state['x'], state['y']
    return vector({'x': x**2, 'y': y**2})  # Source flow

point = vector({'x': 2.0, 'y': 3.0})

div1 = divergence(incompressible_flow, point)
div2 = divergence(compressible_flow, point)

print(f"Rotational flow divergence: {div1:.4f} (should be 0)")
print(f"Source flow divergence: {div2:.4f} (should be 10)")
```

## Project Structure

```bash
KBTU-python-2-final/
├── build/                      # Сборка
├── diffeq/                     # Основная библиотека
│   ├── __pycache__/           # Кэш Python
│   ├── __init__.py
│   ├── SDE.py                 # Системы и интеграторы
│   ├── plotting/              # Визуализация
│   │   ├── __init__.py
│   │   ├── drawing_utils.py
│   │   └── visualization_tasks.py
│   └── utils/                 # Утилиты
│       ├── __pycache__/
│       ├── __init__.py
│       ├── calculus.py        # Численные методы (Якобиан, дивергенция)
│       ├── string_operations.py
│       ├── symbolic.py        # Символьные вычисления
│       └── vectors.py         # Векторные операции
├── diffeq_lib.egg-info/       # Метаданные пакета
├── dist/                      # Дистрибутивы
├── tests/                     # Тесты
│   └── test_numerical_methods.py
├── .gitignore                 # Игнорируемые файлы Git
├── example2.py                # Примеры использования
├── examples.ipynb             # Jupyter notebook с примерами
├── pyproject.toml             # Конфигурация сборки
├── README.md                  # Документация
├── setup.py                   # Конфигурация установки
└── tasks.md                   # Задачи
```

## Testing
```bash

python tests/test_numerical_methods.py
```

## Building from Source
```bash

#installing build tools
pip install build wheel

#building the distribution
python -m build --wheel

#the wheel file will be created in dist/diffeq_lib-0.1.0-py3-none-any.whl
```

