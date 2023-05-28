from geojsonObject import GeoJsonObject

class Point(GeoJsonObject):

    def __init__(self, coordinate):
        self.coordinate = coordinate
    