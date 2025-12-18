import turtle
import math

def draw_phase_portrait(trajectories, x_range=(-5,5), y_range=(-5,5), colors=None):
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.title("Фазовый портрет")
    axis = turtle.Turtle()
    axis.hideturtle()
    axis.speed(0)
    axis.color("gray")
    axis.penup()
    axis.goto(-350,0)
    axis.pendown()
    axis.goto(350,0)
    axis.penup()
    axis.goto(0,-250)
    axis.pendown()
    axis.goto(0,250)
    def scale(x,y):
        sx = (x - x_range[0]) / (x_range[1]-x_range[0])*700 - 350
        sy = (y - y_range[0]) / (y_range[1]-y_range[0])*500 - 250
        return sx, sy

    turt = turtle.Turtle()
    turt.hideturtle()
    turt.speed(0)

    if colors is None:
        colors = ["red","purple","orange","magenta","cyan"]

    for i, traj in enumerate(trajectories):
        if not traj:
            continue
        turt.color(colors[i%len(colors)])
        sx, sy = scale(*traj[0])
        turt.penup()
        turt.goto(sx, sy)
        turt.pendown()
        for x,y in traj[1:]:
            sx, sy = scale(x,y)
            turt.goto(sx, sy)

    screen.update()
    turtle.done()

#создаём траектории для затухающего осциллятора
def generate_spiral_trajectories():
    trajectories = []
    for x0, y0 in [(4,0), (3,2), (2,-3), (-3,3)]:
        traj = []
        x, y = x0, y0
        dt = 0.05
        for _ in range(400):  
            dx = y
            dy = -x - 0.2*y
            x += dx*dt
            y += dy*dt
            traj.append((x,y))
        trajectories.append(traj)
    return trajectories

if __name__ == "__main__":
    trajectories = generate_spiral_trajectories()
    draw_phase_portrait(trajectories)
