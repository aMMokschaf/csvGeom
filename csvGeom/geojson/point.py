from csvGeom.enums.outputType import OutputType


class Point:

    def __init__(self):
        self.coordinates = []
        self.type = OutputType.POINT

    def add_coordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def returnCoordinates(self):
        return self.coordinates[0]

    def __str__(self):
        return f'"type": "{OutputType.POINT.get_geo_json_case()}", "coordinates": {self.returnCoordinates()}'

    def __repr__(self):
        return str(self)

    def __dict__(self):
        return {
            'type': OutputType.POINT.value,
            'coordinates': self.coordinates
        }
