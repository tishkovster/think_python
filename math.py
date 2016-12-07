import math

def pythTriangle(a,b):
    return math.sqrt(a*a + b*b)


a=float(input("Enter one side lenght"))
b=float(input("Enter the other side lenght"))
print(pythTriangle(a,b))
