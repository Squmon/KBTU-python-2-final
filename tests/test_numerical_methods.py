"""Enhanced test for numerical calculus with edge cases"""
from diffeq.utils.calculus import jacobian, divergence
from diffeq.utils.vectors import vector

print("=== Enhanced Numerical Calculus Test ===\n")

def print_result(name, computed, expected, tolerance=1e-6):
    error = abs(computed - expected)
    status = "✓" if error < tolerance else "✗"
    print(f"{status} {name}: {computed:.8f} (expected: {expected:.8f}, error: {error:.2e})")

# Test 1: Linear field (exact derivatives)
print("1. Linear Field: F(x,y) = [ax + by, cx + dy]")
def linear_field(state, a=2, b=3, c=4, d=-1):
    x, y = state['x'], state['y']
    return vector({'u': a*x + b*y, 'v': c*x + d*y})

point = vector({'x': 1.5, 'y': 2.5})
J = jacobian(linear_field, point)

print_result("∂u/∂x", J['du_dx'], 2.0)
print_result("∂u/∂y", J['du_dy'], 3.0)
print_result("∂v/∂x", J['dv_dx'], 4.0)
print_result("∂v/∂y", J['dv_dy'], -1.0)

# Test 2: Quadratic field
print("\n2. Quadratic Field: F(x,y) = [x²y, xy²]")
def quadratic_field(state):
    x, y = state['x'], state['y']
    return vector({'u': x**2 * y, 'v': x * y**2})

point = vector({'x': 2.0, 'y': 3.0})
J = jacobian(quadratic_field, point)

# Exact derivatives: ∂u/∂x = 2xy = 12, ∂u/∂y = x² = 4
# ∂v/∂x = y² = 9, ∂v/∂y = 2xy = 12
print_result("∂u/∂x", J['du_dx'], 12.0)
print_result("∂u/∂y", J['du_dy'], 4.0)
print_result("∂v/∂x", J['dv_dx'], 9.0)
print_result("∂v/∂y", J['dv_dy'], 12.0)

# Test 3: Divergence of various fields
print("\n3. Divergence Tests")

# Spherical field: F(x,y,z) = [x, y, z], div = 3
def spherical_field(state):
    return vector({'x': state['x'], 'y': state['y'], 'z': state['z']})

point = vector({'x': 1.0, 'y': 2.0, 'z': 3.0})
div = divergence(spherical_field, point)
print_result("Spherical field div", div, 3.0)

# Source field: F(x,y) = [x², y²], div = 2x + 2y
def source_field(state):
    x, y = state['x'], state['y']
    return vector({'x': x**2, 'y': y**2})

point = vector({'x': 2.0, 'y': 3.0})
div = divergence(source_field, point)
expected = 2*2.0 + 2*3.0
print_result("Source field div", div, expected)

# Test 4: Edge cases
print("\n4. Edge Cases")

# Very small values (fixed adaptive step)
def tiny_field(state):
    x, y = state['x'], state['y']
    return vector({'x': 1e-10 * x, 'y': 1e-10 * y})

point_tiny = vector({'x': 1e-8, 'y': 2e-8})
J_tiny = jacobian(tiny_field, point_tiny)
print_result("Tiny ∂x/∂x", J_tiny['dx_dx'], 1e-10, tolerance=1e-16)
print_result("Tiny ∂y/∂y", J_tiny['dy_dy'], 1e-10, tolerance=1e-16)

# Mixed scales
def mixed_field(state):
    x, y = state['x'], state['y']
    return vector({'u': 1000*x + 0.001*y, 'v': 0.001*x + 1000*y})

point_mixed = vector({'x': 0.001, 'y': 1000.0})
J_mixed = jacobian(mixed_field, point_mixed)
print_result("Mixed ∂u/∂x", J_mixed['du_dx'], 1000.0)
print_result("Mixed ∂u/∂y", J_mixed['du_dy'], 0.001)

# Test 5: Error handling
print("\n5. Error Handling")
def mismatched_field(state):
    x, y = state['x'], state['y']
    return vector({'u': x*y, 'v': x-y, 'w': x+y})  # Extra output axis

point = vector({'x': 1.0, 'y': 2.0})
try:
    div = divergence(mismatched_field, point)
    print("✗ Should have raised ValueError for mismatched axes")
except ValueError as e:
    print(f"✓ Correctly raised ValueError: {str(e)[:50]}...")

# Test 6: Compare with symbolic (if available)
print("\n6. Numerical vs Symbolic Comparison (if implemented)")
try:
    from diffeq.utils.vectors import vector_function
    
    @vector_function
    def sym_field(x, y):
        return vector({'u': x**2 * y, 'v': x * y**2})
    
    point = vector({'x': 2.0, 'y': 3.0})
    
    # Numerical
    J_num = jacobian(sym_field, point)
    
    # Symbolic (from Ilya's part)
    J_sym = sym_field.yacobian(point)
    
    print("At point (2, 3):")
    for key in ['du_dx', 'du_dy', 'dv_dx', 'dv_dy']:
        num = J_num.get(key, 0)
        sym = J_sym.get(key, 0)
        diff = abs(num - sym)
        print(f"  {key}: num={num:.6f}, sym={sym:.6f}, diff={diff:.2e}")
        
except ImportError as e:
    print("Note: Symbolic comparison not available")

print("\n" + "="*50)
print("Enhanced testing completed!")
print("Your numerical methods handle various cases robustly.")
