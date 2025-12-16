from diffeq.utils.vectors import vector

def jacobian(F, x: vector, h=None):
    """
    Numerical Jacobian of vector function F at point x.

    Returns:
        vector: Keys are 'd{out}_d{in}' containing ∂F_out/∂x_in
    """
    in_axes = list(x.keys())
    Fx = F(x)
    out_axes = list(Fx.keys())
    
    # Adaptive step size if not provided
    if h is None:
        # Get typical magnitude of x values
        magnitudes = [abs(float(v)) for v in x.values() if v != 0]
        if magnitudes:
            typical_x = max(magnitudes)
            # Use relative step size, but ensure it's not too small
            h_rel = 1e-6 * typical_x
            # Absolute minimum step to avoid underflow
            h_abs = max(1e-12, 1e-8 * typical_x) if typical_x > 0 else 1e-8
            h = max(h_rel, h_abs)
        else:
            # All values are zero
            h = 1e-8
    
    J = vector()
    
    for out in out_axes:
        for inp in in_axes:
            x_forward = vector(x)
            x_backward = vector(x)
            
            x_forward[inp] += h
            x_backward[inp] -= h
            
            F_forward = F(x_forward)[out]
            F_backward = F(x_backward)[out]
            
            # Protect against division by very small h
            if abs(h) < 1e-15:
                h = 1e-8  # Reset to safe minimum
                
            derivative = (F_forward - F_backward) / (2 * h)
            J[f'd{out}_d{inp}'] = derivative
    
    return J


def divergence(F, x: vector, h=None):
    """
    Numerical divergence of vector field F at point x.
    Divergence is only defined when input/output axes match.
    """
    Fx = F(x)
    if set(Fx.keys()) != set(x.keys()):
        raise ValueError(
            f"Output axes {set(Fx.keys())} don't match input axes {set(x.keys())}. "
            "Divergence undefined."
        )
    
    if h is None:
        # Same adaptive logic as jacobian
        magnitudes = [abs(float(v)) for v in x.values() if v != 0]
        if magnitudes:
            typical_x = max(magnitudes)
            h_rel = 1e-6 * typical_x
            h_abs = max(1e-12, 1e-8 * typical_x) if typical_x > 0 else 1e-8
            h = max(h_rel, h_abs)
        else:
            h = 1e-8
    
    div_value = 0.0
    axes = list(x.keys())
    
    for axis in axes:
        x_forward = vector(x)
        x_backward = vector(x)
        
        x_forward[axis] += h
        x_backward[axis] -= h
        
        F_forward = F(x_forward)[axis]
        F_backward = F(x_backward)[axis]
        
        if abs(h) < 1e-15:
            h = 1e-8
            
        div_value += (F_forward - F_backward) / (2 * h)
    
    return div_value