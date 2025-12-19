## Numerical Jacobian & Divergence/Library Packaging

## What I Implemented

### jacobian(F, x: vector, h=None) - Computes numerical Jacobian matrix for vector functions

### divergence(F, x: vector, h=None) - Computes numerical divergence of vector fields

### Library packaging system - setup.py and pyproject.toml for distribution

## Key Features

### Adaptive step sizing - Automatically selects optimal h based on input scale
### Central difference method - O(h²) accuracy using [F(x+h) - F(x-h)]/(2h)
### Error protection - Handles edge cases and validates dimensions
### Full project integration - Works with custom vector class and vector_function decorator
### Production-ready packaging - Complete build system for .whl distribution

## Example Usage
```python

from diffeq.utils.calculus import jacobian, divergence
from diffeq.utils.vectors import vector

# Define vector field
def field(state):
    return vector({'x': state['x']**2, 'y': state['y']**2})

# Analyze at point
point = vector({'x': 2.0, 'y': 3.0})
J = jacobian(field, point)      # Jacobian matrix
div = divergence(field, point)  # Divergence scalar

print(f"∂Fₓ/∂x = {J['dx_dx']:.4f}")  # 4.0
print(f"Divergence = {div:.4f}")     # 10.0
```

## Build & Install
```bash

# Build package
python -m build --wheel

# Install locally
pip install dist/diffeq_lib-0.1.0-py3-none-any.whl

# Verify installation
python -c "from diffeq.utils.calculus import jacobian; print('Installed!')"
```

## Applications

### Stability analysis of differential equations via Jacobian eigenvalues

### Flow field analysis - identify sources/sinks via divergence

### Educational tool - compare numerical vs analytical methods

### Research - analyze chaotic systems like Lorenz attractor

### My implementation provides accurate, robust numerical differentiation that integrates seamlessly with the project's existing vector-based architecture.