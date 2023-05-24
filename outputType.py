from enum import Enum

class OutputType(Enum):
    POLYGON = "polygon"
    LINE = "line"
    POINT = "point"

    def getUpperCase(self):
        return self.value.upper()
    
    def getLowerCase(self):
        return self.value.lower()
    
    def getTitleCase(self):
        return self.value.title()
    
    def getAsSuffix(self):
        return '_' + self.value
    