from geojson.geojsonObject import GeoJsonObject

from enums.outputType import OutputType

class MultiLineString(GeoJsonObject):

    def __init__(self):
        self.lineStrings = []
        self.type = OutputType.MULTI_LINESTRING

    def addLineString(self, lineString):
        self.lineStrings.append(lineString)

    def __str__(self):
        lineStrings = ','.join(str(l.returnCoordinates()) for l in self.lineStrings)

        return f'"type": "{OutputType.MULTI_LINESTRING.getGeoJSONCase()}", "coordinates" : {lineStrings}'
    
    def __repr__(self):
        return str(self)
    
    def __dict__(self):
        return {
            'type': OutputType.MULTI_LINESTRING.value,
            'coordinates': self.lineStrings
        }
    