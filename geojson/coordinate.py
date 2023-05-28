class Coordinate():

    def __init__(self, east, north, height):
        self.east = east
        self.north = north
        self.height = height

    def __str__(self):
        return f"'east' : {self.east} 'north' : {self.north} 'height' : {self.height}"
    
    def __dict__(self):
        return {
            'east' : self.east,
            'north' : self.north,
            'height' : self.height
        }
    