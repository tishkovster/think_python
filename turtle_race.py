import turtle              # 1.  import the modules
import random
wn = turtle.Screen()       # 2.  Create a screen
wn.bgcolor('lightblue')

lance = turtle.Turtle()    # 3.  Create two turtles
andy = turtle.Turtle()
lance.color('red')
andy.color('blue')
lance.shape('turtle')
andy.shape('turtle')

andy.up()                  # 4.  Move the turtles to their starting point
lance.up()
andy.goto(-100,20)
lance.goto(-100,-20)
print (lance.position())
while andy.position() <= (100.0, -20.0) or lance.position() <= (100.0 ,20.0) :
    andy.forward(random.randrange(1,10))# It's showtime! BLEAT
    lance.forward(random.randrange(1,10))
if andy.position() > lance.position():
    print("Andy's win!")
else:
    print ("Lance's win!")
wn.exitonclick()
