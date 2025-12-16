
import sys
import os
current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if current_dir not in sys.path:
    sys.path.append(current_dir)
import turtle
from diffeq.plotting.visualization_tasks import plot_phase_portrait
from diffeq.utils.vectors import vector 
from diffeq.plotting.drawing_utils import save_turtle_image
from diffeq import system, rk4_integrator 
def simple_oscillator_func(**coords):
    x = coords.get('x', 0)
    y = coords.get('y', 0)
    return vector({
        'x': y, 
        'y': -x
    })

def predator_prey_func(**coords):
    a, b, c, d = 0.1, 0.02, 0.2, 0.01 
    x = coords.get('x', 0)
    y = coords.get('y', 0)
    
    if x < 0: x = 0
    if y < 0: y = 0

    return vector({
        'x': a * x - b * x * y, 
        'y': d * x * y - c * y
    })

if __name__ == '__main__':

    initial_states_oscillator = [
        {'x': 3.0, 'y': 0.0},
        {'x': 0.0, 'y': 4.0},
        {'x': -2.0, 'y': 1.0},
    ]

    plot_phase_portrait(
        vector_func_def=simple_oscillator_func, 
        initial_points=initial_states_oscillator, 
        t_end=20, 
        x_range=(-5, 5), 
        y_range=(-5, 5)
    )
    
   