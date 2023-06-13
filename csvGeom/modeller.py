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
from csvGeom.validator import Validator
from csvGeom.utils.logger import Logger

class Modeller():

    def __init__(self, language):
        self.util = Util()
        self.validator = Validator()
        self.logger = Logger()
        self.translations = self.util.loadTranslations(language)

    def createCoordinate(self, row):
        east = row.east.strip()
        north = row.north.strip()
        height = row.height.strip()

        return Coordinate(east, north, height)
    
    def createPointGeometry(self, rowList):
        geometry = None
        coordinates = self.util.getFirstElement(rowList)

        geometry = Point()
        row = self.util.getFirstElement(coordinates)
        coordinate = self.createCoordinate(row)
        
        try:
            self.validator.validateCoordinates([coordinate])
            geometry.addCoordinate(coordinate)
        except:
            self.logger.error(self.translations["err_validation"], [geometry.type])
        
        return geometry

    def createLineStringGeometry(self, rowList):
        geometry = None

        coordinates = self.util.getFirstElement(rowList)

        if (len(coordinates) >= 2):
            geometry = LineString()

            for rows in coordinates:
                coordinate = self.createCoordinate(rows)

                try:
                    self.validator.validateCoordinates([coordinate])
                    geometry.addCoordinate(coordinate)
                except:
                    self.logger.error(self.translations["err_validation"], [geometry.type])

        return geometry

    def createPolygonGeometry(self, rowList):
        geometry = None

        coordinates = self.util.getFirstElement(rowList)

        if (len(coordinates) >= 3):
            geometry = Polygon()

            for rows in coordinates:
                coordinate = self.createCoordinate(rows)

                try:
                    self.validator.validateCoordinates([coordinate])
                    geometry.addCoordinate(coordinate)
                except:
                    self.logger.error(self.translations["err_validation"], [geometry.type])

        return geometry

    def createMultiPointGeometry(self, rowList):
        geometry = None

        geometry = MultiPoint()

        for item in rowList:
            itemGeometry = Point()

            for rows in item:
                coordinate = self.createCoordinate(rows)
                itemGeometry.addCoordinate(coordinate)
                
            try:
                self.validator.validate(itemGeometry)
                geometry.addPoint(itemGeometry)
            except:
                self.logger.error(self.translations["err_validation"], [itemGeometry.type])

        return geometry

    def createMultiLineStringGeometry(self, rowList):
        geometry = None

        geometry = MultiLineString()

        for item in rowList:
            itemGeometry = LineString()

            for rows in item:
                coordinate = self.createCoordinate(rows)
                itemGeometry.addCoordinate(coordinate)

            try:
                self.validator.validate(itemGeometry)
                geometry.addLineString(itemGeometry)
            except:
                self.logger.error(self.translations["err_validation"], [itemGeometry.type])

        return geometry

    def createMultiPolygonGeometry(self, rowList):
        geometry = None

        geometry = MultiPolygon()
        for item in rowList:
            itemGeometry = Polygon()

            for rows in item:
                coordinate = self.createCoordinate(rows)
                itemGeometry.addCoordinate(coordinate)

            try:
                self.validator.validate(itemGeometry)
                geometry.addPolygon(itemGeometry)
            except:
                self.logger.error(self.translations["err_validation"], [itemGeometry.type])

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

        if (len(rowList) >= 2):
            selectedGeometryType = self.switchToMultiGeometry(selectedGeometryType)
        
        geometry = self.createGeometry(rowList, selectedGeometryType)
        if geometry != None:
            firstCoordinateList = self.util.getFirstElement(rowList)
            identifier = self.util.getIdentifierFromList(firstCoordinateList)
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
