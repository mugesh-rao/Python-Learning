import math

h=int(input("Height of Wall: "))
w = int(input("Width of Wall: "))
cover = 5

def paint_calc(height , width , cover):
    area = height*width
    num_cans =  math.ceil(area / cover)
    print(f"You'll need {num_cans} cans of paints! ")


paint_calc(h ,w ,cover )

