from geojson.featureCollection import FeatureCollection
from geojson.feature import Feature
from geojson.point import Point
from geojson.line import Line
from geojson.polygon import Polygon
from geojson.multiPoint import MultiPoint
from geojson.coordinate import Coordinate

from enums.outputType import OutputType

from utils.logger import Logger

class Modeller():

    def __init__(self):
        self.logger = Logger()

    def createCoordinate(self, dictLine):
        east = str(dictLine['East']).replace(' ', '')
        north = str(dictLine['North']).replace(' ', '')
        height = str(dictLine['Height']).replace(' ', '')

        return Coordinate(east, north, height)

    def createGeometry(self, dict, selectedGeometryType):
        geometry = None

        if selectedGeometryType == OutputType.POINT:
            if (len(dict) == 1):
                geometry = Point()
            if (len(dict) > 1):
                geometry = MultiPoint()

            for dictLine in dict:
                coordinate = self.createCoordinate(dictLine)
                geometry.addCoordinate(coordinate)

        if selectedGeometryType == OutputType.LINE:
            if (len(dict) >= 2):
                geometry = Line()

                for dictLine in dict:
                    coordinate = self.createCoordinate(dictLine)
                    geometry.addCoordinate(coordinate)

        if selectedGeometryType == OutputType.POLYGON:
            if (len(dict) >= 3):
                geometry = Polygon()

                for dictLine in dict:
                    coordinate = self.createCoordinate(dictLine)
                    geometry.addCoordinate(coordinate)

        return geometry

    def createFeature(self, dict, selectedGeometryType):
        
        identifier = dict[0]['Attribut1']
        
        geometry = self.createGeometry(dict, selectedGeometryType)
        if geometry != None:
            return Feature(identifier, geometry)
        else:
            return None

    def createFeatures(self, dicts, selectedGeometryType):
        list = []

        for dict in dicts:
            feature = self.createFeature(dict, selectedGeometryType)
            if feature != None:
                list.append(feature)
        
        return list

    def createFeatureCollection(self, dicts, selectedGeometryType):

        featureList = self.createFeatures(dicts, selectedGeometryType)

        return FeatureCollection(featureList)
