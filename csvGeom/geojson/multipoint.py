from csvGeom.geojson.geojsonObject import GeoJsonObject

from csvGeom.enums.outputType import OutputType


class Multipoint(GeoJsonObject):

    def __init__(self):
        super().__init__()
        self.points = []
        self.type = OutputType.MULTI_POINT

    def add_point(self, point):
        self.points.append(point)

    def __str__(self):
        points = ','.join(str(p.returnCoordinates()) for p in self.points)

        return f'"type": "{OutputType.MULTI_POINT.get_geo_json_case()}", "coordinates": [{points}]'

    def __repr__(self):
        return str(self)

    def __dict__(self):
        return {
            'type': OutputType.MULTI_POINT.value,
            'coordinates': self.points
        }
