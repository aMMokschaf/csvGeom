from enum import Enum

class OutputType(Enum):
    POINT = "point"
    LINE = "lineString"
    POLYGON = "polygon"
    MULTI_POINT = "multiPoint"
    MULTI_LINE = "multiLineString"
    MULTI_POLYGON = "multiPolygon"

    def getUpperCase(self):
        return self.value.upper()
    
    def getLowerCase(self):
        return self.value.lower()
    
    def getTitleCase(self):
        return self.value.title()
    
    def getAsSuffix(self):
        return "_" + self.value
    