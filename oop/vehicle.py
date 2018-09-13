class Vehicle:

    def __init__(self, top_speed=100):
        self.top_speed = top_speed
        self.__warnings = [] # to make a method private add a double underscore, this is a convention but not a hard rule

    def __repr__(self):
        print("Printing...")
        return 'Top speed :{}, Warnings: {}'.format(self.top_speed, len(self.__warnings))

    # create a private methods to access warning from inside the class
    def add_warning(self,warning_text):
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)


    # define a getter for accessing the warning
    def get_warnings(self):
        return self.__warnings
    

    # classes hold methods
    def drive(self): # by passing self I get access to the class and all its arguements
        print("This car is in motion at speed of {}".format(self.top_speed))