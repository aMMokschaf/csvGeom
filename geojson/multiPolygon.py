from geojson.geojsonObject import GeoJsonObject

from enums.outputType import OutputType

class MultiPolygon(GeoJsonObject):

    def __init__(self):
        self.polygons = []
        self.type = OutputType.MULTI_POLYGON

    def addPolygon(self, polygon):
        self.polygons.append(polygon)

    def __str__(self):
        return f"'type' : {OutputType.MULTI_POLYGON.getGeoJSONCase()} 'coordinates' : {self.polygons}"
    
    def __repr__(self):
        return str(self)
    
    def __dict__(self):
        return {
            'type' : OutputType.MULTI_POLYGON.value,
            'coordinates': self.polygons
        }
    