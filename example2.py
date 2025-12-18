import turtle
from diffeq.plotting.drawing_utils import setup_canvas
from diffeq.utils.vectors import vector

def harmonic_oscillator_func(**coords):
    x = coords.get('x', 0)
    y = coords.get('y', 0)
    return vector({'x': y, 'y': -x})

def plot_phase_portrait_with_lines(vector_func_def, initial_points, t_end=20, dt=0.05):
    screen, axis, scale = setup_canvas(x_range=(-5, 5), y_range=(-5, 5))
    
    turt = turtle.Turtle()
    turt.hideturtle()
    turt.speed(0)

    colors = ["red", "purple", "orange", "magenta", "cyan"]

    for i, pt in enumerate(initial_points):
        x, y = pt['x'], pt['y']
        sx, sy = scale(x, y)
        turt.penup()
        turt.goto(sx, sy)
        turt.pendown()
        turt.color(colors[i % len(colors)])

        steps = int(t_end / dt)
        for _ in range(steps):
            f = vector_func_def(x=x, y=y)
            x_new = x + dt * f['x']
            y_new = y + dt * f['y']
            sx, sy = scale(x_new, y_new)
            turt.goto(sx, sy)
            x, y = x_new, y_new

    screen.update()

if __name__ == '__main__':
    initial_states = [
        {'x': 3.0, 'y': 0.0},
        {'x': 0.0, 'y': 2.5},
        {'x': -4.0, 'y': 0.0},
        {'x': 0.0, 'y': -3.5},
        {'x': 2.0, 'y': 2.0},
    ]

    plot_phase_portrait_with_lines(harmonic_oscillator_func, initial_states, t_end=20)
    turtle.done()  
