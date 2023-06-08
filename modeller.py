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

    def createCoordinate(self, row):
        east = row.east.replace(' ', '')
        north = row.north.replace(' ', '')
        height = row.height.replace(' ', '')

        return Coordinate(east, north, height)

    def createGeometry(self, rowList, selectedGeometryType):
        geometry = None

        if selectedGeometryType == OutputType.POINT:
            coordinates = rowList[0]

            if (len(coordinates) == 1):
                geometry = Point()
                rows = coordinates[0]
                coordinate = self.createCoordinate(rows)
                geometry.addCoordinate(coordinate)

        if selectedGeometryType == OutputType.LINESTRING:
            coordinates = rowList[0]

            if (len(coordinates) >= 2):
                geometry = LineString()

                for rows in coordinates:
                    coordinate = self.createCoordinate(rows)
                    geometry.addCoordinate(coordinate)

        if selectedGeometryType == OutputType.POLYGON:
            coordinates = rowList[0]

            if (len(coordinates) >= 3):
                geometry = Polygon()

                for rows in coordinates:
                    coordinate = self.createCoordinate(rows)
                    geometry.addCoordinate(coordinate)

        if selectedGeometryType == OutputType.MULTI_POINT:
            geometry = MultiPoint()
            for item in rowList:
                itemGeometry = Point()

                for rows in item:
                    coordinate = self.createCoordinate(rows)
                    itemGeometry.addCoordinate(coordinate)
                    
                geometry.addPoint(itemGeometry)

        if selectedGeometryType == OutputType.MULTI_LINESTRING:
            geometry = MultiLineString()
            for item in rowList:
                itemGeometry = LineString()

                for rows in item:
                    coordinate = self.createCoordinate(rows)
                    itemGeometry.addCoordinate(coordinate)
                    
                geometry.addLineString(itemGeometry)

        if selectedGeometryType == OutputType.MULTI_POLYGON:
            geometry = MultiPolygon()
            for item in rowList:
                itemGeometry = Polygon()

                for rows in item:
                    coordinate = self.createCoordinate(rows)
                    itemGeometry.addCoordinate(coordinate)
                    
                geometry.addPolygon(itemGeometry)

        self.logger.debug(f"Created geometry is: {geometry}")
        return geometry
    
    def createFeature(self, rowList, selectedGeometryType):

        if (len(rowList) >= 2):
            if selectedGeometryType == OutputType.POLYGON:
                selectedGeometryType = OutputType.MULTI_POLYGON

            elif selectedGeometryType == OutputType.LINESTRING:
                selectedGeometryType = OutputType.MULTI_LINESTRING

            elif selectedGeometryType == OutputType.POINT:
                selectedGeometryType = OutputType.MULTI_POINT
            self.logger.debug(f"Set GeometryType to {selectedGeometryType.value}")
        
        self.logger.debug(f"Creating Geometry of type {selectedGeometryType}.")
        geometry = self.createGeometry(rowList, selectedGeometryType)
        if geometry != None:
            identifier = rowList[0][0].identifier
            return Feature(identifier, geometry)
        else:
            return None

    def createFeatures(self, rowLists, selectedGeometryType):
        list = []

        for rowList in rowLists:
            feature = self.createFeature(rowList, selectedGeometryType)
            if feature != None:
                list.append(feature)
        
        return list

    def createFeatureCollection(self, rowLists, selectedGeometryType):

        featureList = self.createFeatures(rowLists, selectedGeometryType)

        return FeatureCollection(featureList)
