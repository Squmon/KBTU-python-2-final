import turtle

def save_turtle_image(screen, filename="plot.eps"):
    """
    Сохраняет текущий рисунок Turtle в файл PostScript (.eps).
    """
    try:
        #для сохранения изображения
        screen.getcanvas().postscript(file=filename)
        print(f"Изображение сохранено в {filename}")
    except Exception as e:
        print(f"Ошибка сохранения изображения: {e}")

#настройка холста
def setup_canvas(width=800, height=600, x_range=(-10, 10), y_range=(-10, 10)):
    screen = turtle.Screen()
    screen.setup(width=width, height=height)
    screen.setworldcoordinates(-width / 2, -height / 2, width / 2, height / 2)
    screen.title("Фазовый Портрет / Траектория")
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()

    def draw_axis(t, length, label):
        t.penup()
        t.goto(-length / 2, 0)
        t.pendown()
        t.forward(length)
        #для стрелки
        t.setheading(t.heading() - 150)
        t.forward(10)
        t.backward(10)
        t.setheading(t.heading() + 300)
        t.forward(10)
        
        #ДЛЯ НАДПИСИ
        t.penup()
        t.goto(length / 2 - 20, 10)
        t.write(label, align="center", font=("Arial", 10, "normal"))

   
    t.color("gray")
    draw_axis(t, width - 50, f"X ({x_range[0]} до {x_range[1]})")
    
    t.left(90)
    draw_axis(t, height - 50, f"Y ({y_range[0]} до {y_range[1]})")
    t.right(90)

    def scale_coords(data_x, data_y):
        """Переводит координаты данных в координаты экрана."""
        plot_width = width - 50
        plot_height = height - 50
        
        #диапазон
        data_x_range = x_range[1] - x_range[0]
        data_y_range = y_range[1] - y_range[0]
        #координаты экрана
        screen_x = (data_x - x_range[0]) * plot_width / data_x_range - plot_width / 2
        screen_y = (data_y - y_range[0]) * plot_height / data_y_range - plot_height / 2
        return screen_x, screen_y
    return screen, t, scale_coords
