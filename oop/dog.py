import datetime


class Animal():
    mammal = True
    noise = "Grunt property"
    size = "large"
    color = "brown"
    hair = "Has long fur"
    animal_details = []

    def santize_input(self, string):
        """ this is a helper function to clean inputs  """
        return string[0].upper()+string[1:].lower()

    def get_color(self):
        """ This is a getter for color attribute """
        return self.color

    def add_animal(self,name, species):
        # always format my inputs when I can
        name = self.santize_input(name)
        species = self.santize_input(species)
        detail = { 
            "name": name,
            "type":species
        }
        today = datetime.date.today()
        date_text = "{today.month}/{today.day}/{today.year}".format(today=today)
        detail['date'] = date_text
        self.animal_details.append(detail)
        return detail["name"], detail["type"], detail["date"]
    
    # a property allows me to call a funtion without parenthesis
    @property  
    def make_noise(self):
        return self.noise

class Dog(Animal):
    """ This is a class definition with its inheritance, attributes, and methods  """
    name =  "Jon"
    color = 'brown'

    # this is a model for a function definition
    def some_func(self,arg_1, arg_2, arg_3, kwarg_1=None):
        pass

    # create a getter
    def get_color(self):
        """ This is a getter, it retrieves a value for an accessible attribute """
        print("The color is {}".format(self.color))
        return self.color

    def set_color(self,color):
        """ This is a setter to set the a new value for an attribute """
        self.color = color
        print("Log: The new color is {}".format(self.color))


instance = Dog()
obj = Dog()

# I can set an object outside a functiont directly to the public attribute in python
obj.color = "green"


obj.set_color("orange")

print(obj.make_noise)


print(obj.add_animal("fido","golden retriever"))
