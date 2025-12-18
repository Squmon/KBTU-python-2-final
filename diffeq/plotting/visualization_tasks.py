import turtle
import math

from diffeq.plotting.drawing_utils import setup_canvas
from diffeq import system, rk4_integrator
from diffeq.utils.vectors import vector, vector_function

# ======================
# ВСПОМОГАТЕЛЬНОЕ
# ======================

def _history_to_xy_evolution(history, x_name="x", y_name="y"):
    xs = history.get(x_name, [])
    ys = history.get(y_name, [])
    return list(zip(xs, ys))

# ======================
# ТРАЕКТОРИЯ
# ======================

def plot_trajectory(xy, scale, turt, color="red", thickness=1):
    if not xy:
        return

    turt.color(color)
    turt.pensize(thickness)

    x0, y0 = xy[0]
    sx, sy = scale(x0, y0)

    turt.penup()
    turt.goto(sx, sy)
    turt.pendown()

    for x, y in xy[1:]:
        sx, sy = scale(x, y)
        turt.goto(sx, sy)

# ======================
# ВЕКТОРНОЕ ПОЛЕ
# ======================

def plot_vector_field(vf_xy, scale, x_range, y_range, spacing=0.8, scale_factor=15):
    vec = turtle.Turtle()
    vec.hideturtle()
    vec.speed(0)
    vec.color("blue")
    vec.pensize(1)

    x = x_range[0]
    while x <= x_range[1]:
        y = y_range[0]
        while y <= y_range[1]:
            try:
                dx, dy = vf_xy(x, y)
            except Exception:
                y += spacing
                continue

            mag = math.sqrt(dx**2 + dy**2)
            if mag > 0:
                sx, sy = scale(x, y)
                vec.penup()
                vec.goto(sx, sy)
                vec.setheading(vec.towards(sx + dx, sy + dy))
                vec.pendown()
                vec.forward(min(mag, 1) * scale_factor)

            y += spacing
        x += spacing

# ======================
# ФАЗОВЫЙ ПОРТРЕТ
# ======================

def plot_phase_portrait(
    vector_func_def,
    initial_points,
    t_end=10,
    dt=0.01,
    solver_class=rk4_integrator,
    x_range=(-5, 5),
    y_range=(-5, 5)
):
    screen, axis, scale = setup_canvas(x_range=x_range, y_range=y_range)

    # ❗ УБИРАЕМ ВСЮ АНИМАЦИЮ
    screen.tracer(0, 0)

    # векторное поле
    plot_vector_field(
        lambda x, y: (
            vector_func_def(x=x, y=y).get("x", 0),
            vector_func_def(x=x, y=y).get("y", 0)
        ),
        scale,
        x_range,
        y_range
    )

    vf = vector_function(vector_func_def)
    colors = ["red", "purple", "orange", "magenta", "cyan"]

    x_axis = list(initial_points[0].keys())[0]
    y_axis = list(initial_points[0].keys())[1]

    turt = turtle.Turtle()
    turt.hideturtle()
    turt.speed(0)

    for i, init in enumerate(initial_points):
        solver = solver_class(dt)
        initials = vector(init)
        ode = system(vf, solver, initials=initials)

        history = ode.run(t_end)
        xy = _history_to_xy_evolution(history, x_axis, y_axis)

        plot_trajectory(
            xy,
            scale,
            turt,
            color=colors[i % len(colors)],
            thickness=1
        )

    screen.update()
    turtle.done()
