from geojson.geojsonObject import GeoJsonObject

from enums.outputType import OutputType

class MultiPoint(GeoJsonObject):

    def __init__(self):
        self.points = []
        self.type = OutputType.MULTI_POINT

    def addPoint(self, point):
        self.points.append(point)

    def __str__(self):
        points = ','.join(str(p.returnCoordinate()) for p in self.points)

        return f'"type": "{OutputType.MULTI_POINT.getGeoJSONCase()}", "coordinates": {points}'
    
    def __repr__(self):
        return str(self)
    
    def __dict__(self):
        return {
            'type': OutputType.MULTI_POINT.value,
            'coordinates': self.points
        }
    