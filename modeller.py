from geojson.featureCollection import FeatureCollection
from geojson.feature import Feature
from geojson.point import Point
from geojson.lineString import LineString
from geojson.multiLineString import MultiLineString
from geojson.polygon import Polygon
from geojson.multiPolygon import MultiPolygon
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
            coordinates = dict[0]

            if (len(coordinates) == 1):
                geometry = Point()
                dictLine = coordinates[0]
                coordinate = self.createCoordinate(dictLine)
                geometry.addCoordinate(coordinate)

        if selectedGeometryType == OutputType.LINESTRING:
            coordinates = dict[0]

            if (len(coordinates) >= 2):
                geometry = LineString()

                for dictLine in coordinates:
                    coordinate = self.createCoordinate(dictLine)
                    geometry.addCoordinate(coordinate)

        if selectedGeometryType == OutputType.POLYGON:
            coordinates = dict[0]

            if (len(coordinates) >= 3):
                geometry = Polygon()

                for dictLine in coordinates:
                    coordinate = self.createCoordinate(dictLine)
                    geometry.addCoordinate(coordinate)

        if selectedGeometryType == OutputType.MULTI_POINT:
            geometry = MultiPoint()
            for item in dict:
                itemGeometry = Point()

                for dictLine in item:
                    coordinate = self.createCoordinate(dictLine)
                    itemGeometry.addCoordinate(coordinate)
                    
                geometry.addPoint(itemGeometry)

        if selectedGeometryType == OutputType.MULTI_LINESTRING:
            geometry = MultiLineString()
            for item in dict:
                itemGeometry = LineString()

                for dictLine in item:
                    coordinate = self.createCoordinate(dictLine)
                    itemGeometry.addCoordinate(coordinate)
                    
                geometry.addLineString(itemGeometry)

        if selectedGeometryType == OutputType.MULTI_POLYGON:
            geometry = MultiPolygon()
            for item in dict:
                itemGeometry = Polygon()

                for dictLine in item:
                    coordinate = self.createCoordinate(dictLine)
                    itemGeometry.addCoordinate(coordinate)
                    
                geometry.addPolygon(itemGeometry)

        self.logger.debug(f"Created geometry is: {geometry}")
        return geometry
    
    def createFeature(self, dict, selectedGeometryType):

        if (len(dict) >= 2):
            if selectedGeometryType == OutputType.POLYGON:
                selectedGeometryType = OutputType.MULTI_POLYGON

            elif selectedGeometryType == OutputType.LINESTRING:
                selectedGeometryType = OutputType.MULTI_LINESTRING

            elif selectedGeometryType == OutputType.POINT:
                selectedGeometryType = OutputType.MULTI_POINT
            self.logger.debug(f"Set GeometryType to {selectedGeometryType.value}")
        
        self.logger.debug(f"Creating Geometry of type {selectedGeometryType}.")
        geometry = self.createGeometry(dict, selectedGeometryType)
        if geometry != None:
            identifier = dict[0][0]['Attribut1']
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
