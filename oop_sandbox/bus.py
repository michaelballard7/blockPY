from vehicle import Vehicle


class Bus(Vehicle):
    
    def __init__(self, starting_top_speed=65):
        super().__init__(starting_top_speed) # super calls the parent constructor of the base class
        
        self.passengers = []


    def add_group(self, passengers):
        self.passengers.extend(passengers)