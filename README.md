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

python -c "from diffeq.utils.calculus import jacobian, divergence; print('Your numerical calculus methods are installed!')"
```

## Project Structure

```bash
KBTU-python-2-final/
├── build/                      # Build artifacts
├── diffeq/                     # Main library
│   ├── __pycache__/            # Python cache
│   ├── __init__.py
│   ├── SDE.py                  # Systems and integrators
│   ├── plotting/               # Visualization
│   │   ├── __init__.py
│   │   ├── drawing_utils.py
│   │   └── visualization_tasks.py
│   └── utils/                  # Utilities
│       ├── __pycache__/
│       ├── __init__.py
│       ├── calculus.py         # Numerical methods (Jacobian, divergence)
│       ├── string_operations.py
│       ├── symbolic.py         # Symbolic computations
│       └── vectors.py          # Vector operations
├── diffeq_lib.egg-info/        # Package metadata
├── dist/                       # Distribution files
├── tests/                      # Tests
│   └── test_numerical_methods.py
├── .gitignore                  # Git ignore files
├── example2.py                 # Usage examples
├── examples.ipynb              # Jupyter notebook with examples
├── pyproject.toml              # Build configuration
├── README.md                   # Documentation
├── setup.py                    # Installation configuration
└── tasks.md                    # Tasks
```

## Testing

### Jacobian & Divergence (numerical methods) 
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

