import turtle
import math
import random

fred = turtle.Turtle()
fred.up()
fred.tracer(1000)
wn = turtle.Screen()
wn.setworldcoordinates(-1, -1, 1, 1)

numdarts = 10000
insideCount = 0
for i in range(numdarts):
    randx = random.uniform(-1, 1)
    randy = random.uniform(-1, 1)

    x = randx
    y = randy
    fred.penup()
    fred.goto(randx, randy)
    if fred.distance(0, 0) <= 1:
        fred.color("red")
        insideCount += 1
    else:
        fred.color("blue")
        # print(fred.distance(0,0))
    fred.dot()
pii= (float(insideCount)/ float(numdarts))
fred.pencolor('black')
print(pii *4)
wn.exitonclick()
