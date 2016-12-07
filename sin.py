import math
import turtle

wn = turtle.Screen()
wn.bgcolor('lightblue')
wn.setworldcoordinates(0,-1.25,360,1.25)
fred = turtle.Turtle()

for angle in range(360):
    fred.goto(angle,math.sin(math.radians(angle)))
#your code here

wn.exitonclick()
