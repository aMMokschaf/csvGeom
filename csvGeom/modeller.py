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

from csvGeom.utils.util import Util

class Modeller():

    def __init__(self, language, logger):
        self.util = Util()
        self.logger = logger
        self.translations = self.util.loadTranslations(language)

    def createCoordinate(self, row):
        ptId = row.id.strip()
        east = row.east.strip()
        north = row.north.strip()
        height = row.height.strip()

        return Coordinate(ptId, east, north, height)
    
    def createPointGeometry(self, rowList):
        geometry = None
        coordinates = self.util.getFirstElement(rowList)

        geometry = Point()
        row = self.util.getFirstElement(coordinates)
        coordinate = self.createCoordinate(row)

        geometry.addCoordinate(coordinate)
        
        return geometry

    def createLineStringGeometry(self, rowList):
        geometry = None

        coordinates = self.util.getFirstElement(rowList)

        geometry = LineString()

        for rows in coordinates:
            coordinate = self.createCoordinate(rows)

            geometry.addCoordinate(coordinate)

        return geometry

    def createPolygonGeometry(self, rowList):
        geometry = None

        coordinates = self.util.getFirstElement(rowList)

        geometry = Polygon()

        for rows in coordinates:
            coordinate = self.createCoordinate(rows)

            geometry.addCoordinate(coordinate)

        return geometry

    def createMultiPointGeometry(self, rowList):
        geometry = None

        geometry = MultiPoint()

        for item in rowList:
            itemGeometry = Point()

            for rows in item:
                coordinate = self.createCoordinate(rows)
                itemGeometry.addCoordinate(coordinate)
                geometry.addPoint(itemGeometry)

        return geometry

    def createMultiLineStringGeometry(self, rowList):
        geometry = None

        geometry = MultiLineString()

        for item in rowList:
            itemGeometry = LineString()

            for rows in item:
                coordinate = self.createCoordinate(rows)
                itemGeometry.addCoordinate(coordinate)
                geometry.addLineString(itemGeometry)

        return geometry

    def createMultiPolygonGeometry(self, rowList):
        geometry = None

        geometry = MultiPolygon()
        for item in rowList:
            itemGeometry = Polygon()

            for rows in item:
                coordinate = self.createCoordinate(rows)
                itemGeometry.addCoordinate(coordinate)
                geometry.addPolygon(itemGeometry)

        return geometry

    def createGeometry(self, rowList, selectedGeometryType):

        if selectedGeometryType == OutputType.POINT:
            return self.createPointGeometry(rowList)

        if selectedGeometryType == OutputType.LINESTRING:
            return self.createLineStringGeometry(rowList)

        if selectedGeometryType == OutputType.POLYGON:
            return self.createPolygonGeometry(rowList)

        if selectedGeometryType == OutputType.MULTI_POINT:
            return self.createMultiPointGeometry(rowList)

        if selectedGeometryType == OutputType.MULTI_LINESTRING:
            return self.createMultiLineStringGeometry(rowList)

        if selectedGeometryType == OutputType.MULTI_POLYGON:
            return self.createMultiPolygonGeometry(rowList)
        
    def switchToMultiGeometry(self, selectedGeometryType):
        if selectedGeometryType == OutputType.POLYGON:
            return OutputType.MULTI_POLYGON

        elif selectedGeometryType == OutputType.LINESTRING:
            return OutputType.MULTI_LINESTRING

        elif selectedGeometryType == OutputType.POINT:
            return OutputType.MULTI_POINT
    
    def createFeature(self, rowList, selectedGeometryType):
        
        geometry = self.createGeometry(rowList, selectedGeometryType)
        if geometry != None:
            firstCoordinateList = self.util.getFirstElement(rowList)
            identifier = self.util.getIdentifierFromList(firstCoordinateList)
            return Feature(identifier, geometry)
        else:
            return None
        
    def transformRowListForMultiPoint(self, rowList):
        list = []

        for subList in rowList:
            for coordinate in subList:
                list2 = []
                list2.append(coordinate)
                list.append(list2)

        return list

    def createFeatures(self, rowLists, selectedGeometryType):
        list = []

        for rowList in rowLists:

            geometryType = None

            feature = None

            if selectedGeometryType == OutputType.POINT and len(rowList[0]) >= 2:

                geometryType = self.switchToMultiGeometry(selectedGeometryType)

                transformedList = self.transformRowListForMultiPoint(rowList)

                feature = self.createFeature(transformedList, geometryType)
                
            else:

                if (len(rowList) >= 2):
                    geometryType = self.switchToMultiGeometry(selectedGeometryType)
                else:
                    geometryType = selectedGeometryType

                feature = self.createFeature(rowList, geometryType)

            if feature != None:
                list.append(feature)
        
        return list

    def createFeatureCollection(self, rowLists, selectedGeometryType):

        featureList = self.createFeatures(rowLists, selectedGeometryType)

        featureCollection = FeatureCollection()

        featureCollection.features = featureList

        return featureCollection
