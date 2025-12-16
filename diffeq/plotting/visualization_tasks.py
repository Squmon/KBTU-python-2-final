import turtle
import math

from diffeq.plotting.drawing_utils import setup_canvas, save_turtle_image 
from diffeq import system, rk4_integrator 
from diffeq.utils.vectors import vector, vector_function
def _history_to_xy_evolution(history_vector, x_axis_name='x', y_axis_name='y'):

    x_list = history_vector.get(x_axis_name, [])
    y_list = history_vector.get(y_axis_name, [])
    return list(zip(x_list, y_list))

def plot_trajectory(xy_evolution, color="red", line_thickness=2, x_range=None, y_range=None):
    if not xy_evolution:
        print("Ошибка: Список координат пуст.")
        return

    # Вычисляем диапазоны
    if x_range is None:
        all_x = [p[0] for p in xy_evolution]
        x_range = (min(all_x) - 0.1, max(all_x) + 0.1) 
    if y_range is None:
        all_y = [p[1] for p in xy_evolution]
        y_range = (min(all_y) - 0.1, max(all_y) + 0.1)
        
    screen, t, scale = setup_canvas(x_range=x_range, y_range=y_range)
    t.color(color)
    t.pensize(line_thickness)
    
    start_x, start_y = xy_evolution[0]
    screen_start_x, screen_start_y = scale(start_x, start_y)
    t.penup()
    t.goto(screen_start_x, screen_start_y)
    t.dot(5, "green") # Начальная точка
    t.pendown()
    
    for x, y in xy_evolution[1:]:
        screen_x, screen_y = scale(x, y)
        t.goto(screen_x, screen_y)
    
    t.dot(5, color) # Конечная точка
    
    print(f"Траектория ({color}) успешно построена.")


def plot_vector_field(vector_function, x_range=(-5, 5), y_range=(-5, 5), spacing=1.0, scale_factor=20):
    screen, t, scale = setup_canvas(x_range=x_range, y_range=y_range)
    
    t.color("blue")
    t.pensize(1)
    vec_drawer = turtle.Turtle()
    vec_drawer.hideturtle()
    vec_drawer.speed(0)
    vec_drawer.color("blue")
    x_min, x_max = x_range
    y_min, y_max = y_range
    x = x_min
    while x <= x_max:
        y = y_min
        while y <= y_max:
            
            try:
                dx_dt, dy_dt = vector_function(x, y) 
            except Exception as e:
                y += spacing
                continue

            magnitude = (dx_dt**2 + dy_dt**2)**0.5
            
            if magnitude > 0:
                max_length = 0.5 * spacing 
                vec_length = min(magnitude, max_length) * scale_factor / max_length
                # Рисуем вектор

                start_sx, start_sy = scale(x, y)
                angle = vec_drawer.towards(dx_dt, dy_dt) 
                vec_drawer.penup()
                vec_drawer.goto(start_sx, start_sy)
                vec_drawer.setheading(angle)
                vec_drawer.pendown()
                vec_drawer.forward(vec_length)
                # Рисуем стрелку
                vec_drawer.pensize(0.5)
                vec_drawer.setheading(angle - 135)
                vec_drawer.forward(3)
                vec_drawer.backward(3)
                vec_drawer.setheading(angle + 135)
                vec_drawer.forward(3)
                vec_drawer.pensize(1)
                
            y += spacing
        x += spacing
    
    print("Векторное поле успешно построено.")



def plot_phase_portrait(vector_func_def, initial_points=None, t_end=10, dt=0.01, solver_class=rk4_integrator, x_range=(-5, 5), y_range=(-5, 5)):
    
    # 1. СОЗДАНИЕ ОБЕРТКИ для plot_vector_field (БЕЗ ИЗМЕНЕНИЙ ЗДЕСЬ)
    def vector_field_wrapper(x, y):
        v = vector_func_def(x=x, y=y)
        return v.get('x', 0), v.get('y', 0) 
    
    # 2. ВЫЗОВ plot_vector_field (БЕЗ ИЗМЕНЕНИЙ ЗДЕСЬ)
    plot_vector_field(
        lambda x, y: (vector_func_def(x=x, y=y).get('x', 0), vector_func_def(x=x, y=y).get('y', 0)),
        x_range=x_range, 
        y_range=y_range, 
        spacing=0.8, 
        scale_factor=15
    )
    
    # ... (Остальной код для траекторий)
    if initial_points and initial_points[0]:
        x_axis = list(initial_points[0].keys())[0] 
        y_axis = list(initial_points[0].keys())[1] 
        vf = vector_function(vector_func_def)
        colors = ["red", "purple", "orange", "magenta", "cyan"]
        for i, initial_state_dict in enumerate(initial_points):
            color = colors[i % len(colors)]
            
            # Инициализируем систему
            solver = solver_class(dt)
            initials = vector(initial_state_dict)
            
            # ИЗМЕНЕНИЕ 1: sys -> ode_sys
            ode_sys = system(vf, solver, initials=initials)
            
            # Вычисляем эволюцию
            # ИЗМЕНЕНИЕ 2: sys.run -> ode_sys.run
            history_vec = ode_sys.run(t_end)
            
            #преобразуем историю в список (x, y)
            xy_evolution = _history_to_xy_evolution(history_vec, x_axis, y_axis)
            
            #рисуем траекторию
            plot_trajectory(
                xy_evolution, 
                color=color, 
                x_range=x_range, 
                y_range=y_range, 
                line_thickness=1
            )
        print(f"Построено {len(initial_points)} траекторий, используя {solver_class.__name__}.")
        turtle.done()