import turtle

def save_turtle_image(screen, filename="plot.eps"):
    try:
        screen.getcanvas().postscript(file=filename)
        print(f"Изображение сохранено в {filename}")
    except Exception as e:
        print(f"Ошибка сохранения изображения: {e}")


def setup_canvas(width=800, height=600, x_range=(-10, 10), y_range=(-10, 10)):
    screen = turtle.Screen()
    screen.setup(width=width, height=height)
    screen.title("Фазовый портрет")

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.color("gray")

    # OX
    t.penup()
    t.goto(-width / 2 + 25, 0)
    t.pendown()
    t.goto(width / 2 - 25, 0)
    t.write("X", align="right")

    # OY
    t.penup()
    t.goto(0, -height / 2 + 25)
    t.pendown()
    t.goto(0, height / 2 - 25)
    t.write("Y", align="left")

    #масштабирование координат
    def scale_coords(data_x, data_y):
        plot_width = width - 50
        plot_height = height - 50

        data_x_range = x_range[1] - x_range[0]
        data_y_range = y_range[1] - y_range[0]

        screen_x = (data_x - x_range[0]) * plot_width / data_x_range - plot_width / 2
        screen_y = (data_y - y_range[0]) * plot_height / data_y_range - plot_height / 2

        return screen_x, screen_y

    return screen, t, scale_coords
