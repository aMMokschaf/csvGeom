from utils.util import Util
from enums.outputType import OutputType

class OutputFormatter():

    def __init__(self):
        self.util = Util()

    def createSingleCoord(self, coordinates, minIndent):
        util = self.util

        point = util.indent(minIndent) + '['
        point += util.indent(minIndent + 1) + coordinates.east + ','
        point += util.indent(minIndent + 1) + coordinates.north + ','
        point += util.indent(minIndent + 1) + coordinates.height
        point += util.indent(minIndent) + ']'
        
        return point

    def createFeatureHeader(self, identifier, geometryType):
        util = self.util
        
        header = util.indent(2) + '{'
        header += util.indent(3) + '"type": "Feature",'
        header += util.indent(3) + '"properties": {'
        header += util.indent(4) + f'"identifier": "{identifier}"'
        header += util.indent(3) + '},'
        header += util.indent(3) + '"geometry": {'

        geometryType = OutputType(geometryType).getGeoJSONCase()

        header += util.indent(4) + f'"type": "{geometryType}",'

        return header

    def createFeatureFooter(self):
        util = self.util

        footer = util.indent(3) + '}'
        footer += util.indent(2) + '}'

        return footer

    def createFeature(self, feature):

        type = feature.geometry.type
        coordinates = feature.geometry.coordinates

        header = self.createFeatureHeader(feature.identifier, type)

        coords = ""

        if type == OutputType.POINT:
            coords = self.createPointCoords(coordinates)
        elif type == OutputType.LINE:
            coords = self.createLineCoords(feature.geometry.coordinates)
        elif type == OutputType.POLYGON:
            coords = self.createPolygonCoords(coordinates)
        elif type == OutputType.MULTI_POINT:
            coords = self.createMultiPointCoords(coordinates)
        elif type == OutputType.MULTI_LINE:
            pass
        elif type == OutputType.MULTI_POLYGON:
            pass
        
        footer = self.createFeatureFooter()

        return header + coords + footer
    
    def createPointCoords(self, coordinates):
        util = self.util

        point = util.indent(4) + '"coordinates": '

        for index, element in enumerate(coordinates):
            point += self.createSingleCoord(element, 5)

            if index != len(coordinates)-1:
                point += ','
        
        return point
    
    def createLineCoords(self, coordinates):
        util = self.util

        line = util.indent(4) + '"coordinates": ['

        for index, element in enumerate(coordinates):
            line += self.createSingleCoord(element, 5)

            if index != len(coordinates)-1:
                line += ','

        line += util.indent(4) + ']'

        return line

    def createPolygonCoords(self, coordinates):
        util = self.util

        polygon = util.indent(4) + '"coordinates": ['
        polygon += util.indent(5) + '['

        for index, element in enumerate(coordinates):
            polygon += self.createSingleCoord(element, 6)

            if index != len(coordinates)-1:
                polygon += ','

        polygon += util.indent(5) + ']'
        polygon += util.indent(4) + ']'

        return polygon
    
    def createMultiPointCoords(self, coordinates):
        util = self.util

        point = util.indent(4) + '"coordinates": ['

        for index, element in enumerate(coordinates):
            point += self.createSingleCoord(element, 5)

            if index != len(coordinates)-1:
                point += ','

        point += util.indent(4) + ']'
        
        return point


    def createFeatureCollectionHeader(self, type, name):
        util = self.util

        header = '{'
        header += util.indent(1) + f'"type": "{type}",' 
        header += util.indent(1) + f'"name": "{name}",'
        header += util.indent(1) + '"features": [ '

        return header

    def createFeatureCollectionFooter(self):
        return self.util.indent(1) + ']' + '\n}'
    
    def createFeatures(self, features):
        data = ""

        for index, feature in enumerate(features):
            data += self.createFeature(feature)

            if index != len(features)-1:
                data += ','
        
        return data

    def createFeatureCollection(self, featureCollectionModel):
        data = self.createFeatureCollectionHeader(featureCollectionModel.type, featureCollectionModel.name)

        data += self.createFeatures(featureCollectionModel.features)

        return data + self.createFeatureCollectionFooter()
