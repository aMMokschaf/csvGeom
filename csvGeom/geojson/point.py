from csvGeom.geojson.geojsonObject import GeoJsonObject

from csvGeom.enums.outputType import OutputType

class Point(GeoJsonObject):

    def __init__(self):
        self.coordinate = None
        self.type = OutputType.POINT

    def addCoordinate(self, coordinate):
        self.coordinate = coordinate

    def returnCoordinate(self):
        return self.coordinate

    def __str__(self):
        return f'"type": "{OutputType.POINT.getGeoJSONCase()}", "coordinates": {self.coordinate}'
    
    def __repr__(self):
        return str(self)
    
    def __dict__(self):
        return {
            'type': OutputType.POINT.value,
            'coordinates': self.coordinate
        }