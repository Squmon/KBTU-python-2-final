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

    axis = turtle.Turtle()
    axis.speed(0)
    axis.hideturtle()
    axis.color("gray")

    # OX
    axis.penup()
    axis.goto(-width / 2 + 25, 0)
    axis.pendown()
    axis.goto(width / 2 - 25, 0)
    axis.write("X", align="right")

    # OY
    axis.penup()
    axis.goto(0, -height / 2 + 25)
    axis.pendown()
    axis.goto(0, height / 2 - 25)
    axis.write("Y", align="left")

    def scale_coords(x, y):
        plot_w = width - 50
        plot_h = height - 50

        sx = (x - x_range[0]) * plot_w / (x_range[1] - x_range[0]) - plot_w / 2
        sy = (y - y_range[0]) * plot_h / (y_range[1] - y_range[0]) - plot_h / 2

        return sx, sy

    return screen, axis, scale_coords
