from geojson.featureCollection import FeatureCollection
from geojson.feature import Feature
from geojson.polygon import Polygon
from geojson.point import Point
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

    def createGeometry(self, dict, geometryType):
        geometry = None

        if geometryType == OutputType.POINT:
            geometry = Point()

            for dictLine in dict:
                coordinate = self.createCoordinate(dictLine)
                geometry.addCoordinate(coordinate)

        if geometryType == OutputType.LINE:
            pass

        if geometryType == OutputType.POLYGON:
            geometry = Polygon()

            for dictLine in dict:
                coordinate = self.createCoordinate(dictLine)
                geometry.addCoordinate(coordinate)

        if geometryType == OutputType.MULTI_POINT:
            pass

        if geometryType == OutputType.MULTI_LINE:
            pass

        if geometryType == OutputType.MULTI_POLYGON:
            pass

        return geometry

    def createFeature(self, dict, geometryType):
        
        identifier = dict[0]['Attribut1']
        
        eval = True

        # for now, only notify
        if geometryType == OutputType.POINT and len(dict) > 1:
            self.logger.info(f"More than one coordinate for: {str(identifier)}. Using only first coordinate!")
            dict = dict[0]
            eval = True
        if geometryType == OutputType.LINE and len(dict) < 2:
            self.logger.error(f"Not enough Coordinates for Line: {str(identifier)}")
            eval = False
        if geometryType == OutputType.POLYGON and len(dict) < 3:
            self.logger.error(f"Not enough Coordinates for Polygon: {str(identifier)}")
            eval = False

        if eval == True:
            self.logger.info(f"Success:  {str(identifier)}")
        else:
            self.logger.error(f"Feature {str(identifier)} has invalid geometry!")
        
        geometry = self.createGeometry(dict, geometryType)
        return Feature(identifier, geometry)

    def createFeatures(self, dicts, geometryType):
        list = []

        for dict in dicts:
            feature = self.createFeature(dict, geometryType)
            list.append(feature)
        
        return list

    def createFeatureCollection(self, dicts, geometryType):
        featureList = self.createFeatures(dicts, geometryType)

        return FeatureCollection(featureList)
