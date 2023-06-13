from csvGeom.enums.outputType import OutputType

class Validator():
    
    def __init__(self):
        pass
    
    def determineGeometryType(self, geometry):
        return geometry.type

    def validateNorth(self, value):
        return value != None
    
    def validateEast(self, value):
        return value != None

    def validateCoordinate(self, coordinate):
        return self.validateNorth(coordinate.north) and self.validateEast(coordinate.east)
    
    def validateCoordinates(self, coordinates):
        for coordinate in coordinates:
            if not self.validateCoordinate(coordinate):
                return False

        return True

    def validatePoint(self, geometry):
        numberOfCoordinates = len(geometry.coordinates)

        if numberOfCoordinates != 1:
            raise Exception

    def validateLineString(self, geometry):
        numberOfCoordinates = len(geometry.coordinates)

        if numberOfCoordinates < 2:
            raise Exception

    def validatePolygon(self, geometry):
        numberOfCoordinates = len(geometry.coordinates)

        if numberOfCoordinates < 3:
            raise Exception

    def validate(self, geometry):
        type = self.determineGeometryType(geometry)

        if not self.validateCoordinates(geometry.coordinates):
            raise Exception

        try:
            if type == OutputType.POINT:
                self.validatePoint(geometry)
            elif type == OutputType.LINESTRING:
                self.validateLineString(geometry)
            elif type == OutputType.POLYGON:
                self.validatePolygon(geometry)
        except:
            raise Exception
