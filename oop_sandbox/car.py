
# I have to import the file that I am using for inheritance
from vehicle import Vehicle


class Car(Vehicle):
    pass

   


x = Car(200)
x.drive()

Car.top_speed = 200

y = Car(250)
y.drive()

# print(x)
# if I want to look into an object I can use:
# print(x.__dict__)

print(x.get_warnings())

