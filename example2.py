import turtle
import sys
import os

try:
    current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
except NameError:
    pass


from diffeq.plotting.visualization_tasks import plot_phase_portrait
from diffeq.utils.vectors import vector 
def stable_node_func(**coords):
    x = coords.get('x', 0)
    y = coords.get('y', 0)
    
    # dx/dt = -x
    # dy/dt = -2y
    return vector({
        'x': -x, 
        'y': -2 * y 
    })
if __name__ == '__main__':
    
    initial_states_node = [
        {'x': 5.0, 'y': 5.0},
        {'x': -5.0, 'y': 5.0},
        {'x': 5.0, 'y': -5.0},
        {'x': -5.0, 'y': -5.0},
    ]

    plot_phase_portrait(
        vector_func_def=stable_node_func, 
        initial_points=initial_states_node, 
        t_end=5, 
        x_range=(-6, 6), 
        y_range=(-6, 6)
    )