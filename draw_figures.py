import turtle

def drawPolygon(t, sideLength, numSides):
    for i in range(numSides):
        t.forward(sideLength)
        t.left(360/numSides)# your code here.

def drawColorPolygon(t, sideLength, numSides,color,fillColor):
    t.fill(True)
    t.color(color)
    t.fillcolor(fillColor)
    for i in range(numSides):
        t.forward(sideLength)
        t.left(360/numSides)# your code here
    t.fill(False)

def star(t,sideLength):
    coords=[]
    for i in range(5):
            #t.penup()
            t.forward(sideLength)
            t.left(360/5)
            coords.append(t.position())
    #t.pendown()
    #t.fill(True)
    t.color("red")
    t.fillcolor("red")
    t.goto(coords[1])
    t.goto(coords[3])
    t.goto(coords[0])
    t.goto(coords[2])
    t.goto(coords[4])



legumber=int(input("How many legs do you prefer: ")
#numSides=int(input("Enter number of sides: "))
#sideLengh=int(input("Enter side lenght: "))
#color=input("Enter color: ")
#fillColor=input("Enter fill color:")


wn = turtle.Screen()
geo = turtle.Turtle()
#drawColorPolygon(geo,sideLengh,numSides,color,fillColor)
spider(geo,legumber)
wn.exitonclick()

