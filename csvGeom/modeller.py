from csvGeom.geojson.coordinate import Coordinate
from csvGeom.geojson.feature import Feature
from csvGeom.geojson.featureCollection import FeatureCollection

from csvGeom.geojson.point import Point
from csvGeom.geojson.lineString import LineString
from csvGeom.geojson.polygon import Polygon

from csvGeom.geojson.multiPoint import MultiPoint
from csvGeom.geojson.multiLineString import MultiLineString
from csvGeom.geojson.multiPolygon import MultiPolygon

from csvGeom.enums.outputType import OutputType

from csvGeom.utils.logger import Logger

class Modeller():

    def __init__(self):
        self.logger = Logger()

    def createCoordinate(self, row):
        east = row.east.strip()
        north = row.north.strip()
        height = row.height.strip()

        return Coordinate(east, north, height)

    def createGeometry(self, rowList, selectedGeometryType):
        geometry = None

        if selectedGeometryType == OutputType.POINT:
            coordinates = rowList[0]

            if (len(coordinates) == 1):
                geometry = Point()
                row = coordinates[0]
                coordinate = self.createCoordinate(row)
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

        return geometry
    
    def createFeature(self, rowList, selectedGeometryType):

        if (len(rowList) >= 2):
            if selectedGeometryType == OutputType.POLYGON:
                selectedGeometryType = OutputType.MULTI_POLYGON

            elif selectedGeometryType == OutputType.LINESTRING:
                selectedGeometryType = OutputType.MULTI_LINESTRING

            elif selectedGeometryType == OutputType.POINT:
                selectedGeometryType = OutputType.MULTI_POINT
        
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
