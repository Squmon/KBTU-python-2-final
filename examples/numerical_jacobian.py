from diffeq.utils.calculus import jacobian, divergence
from diffeq.utils.vectors import vector

def format_vector(v, decimals=3):
    """Форматирует вектор с ограничением знаков после запятой"""
    result = vector()
    for key, value in v.items():
        result[key] = f"{value:.{decimals}f}"
    return result

# Define a vector field: F(x,y) = [x*y, x+y]
def field(state):
    x, y = state['x'], state['y']
    return vector({'x': x*y, 'y': x + y})

# Point to evaluate at
point = vector({'x': 2.0, 'y': 3.0})

# Compute Jacobian numerically
J_num = jacobian(field, point)
print("Numerical Jacobian:")
print(format_vector(J_num, 2))

# Compute divergence numerically
div_num = divergence(field, point)
print(f"\nNumerical Divergence: {div_num:.2f}")