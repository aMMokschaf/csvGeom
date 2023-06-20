from csvGeom.enums.outputType import OutputType
from csvGeom.utils.util import Util

from csvGeom.geojson.featureCollection import FeatureCollection
from csvGeom.geojson.feature import Feature
from csvGeom.geojson.coordinate import Coordinate
from csvGeom.geojson.point import Point
from csvGeom.geojson.lineString import LineString
from csvGeom.geojson.polygon import Polygon
from csvGeom.geojson.multiPoint import MultiPoint
from csvGeom.geojson.multiLineString import MultiLineString
from csvGeom.geojson.multiPolygon import MultiPolygon

class Validator():
    
    def __init__(self, logger, language):
        self.logger = logger
        self.errCount = 0

        self.util = Util()
        self.translations = self.util.loadTranslations(language)
    
    def determineGeometryType(self, geometry):
        return geometry.type

    def validateCoordinateElement(self, value):
        return value != None

    def validateCoordinate(self, coordinate):
        return self.validateCoordinateElement(coordinate.north) and self.validateCoordinateElement(coordinate.east)
    
    def validateCoordinates(self, coordinates):
        for coordinate in coordinates:
            if not self.validateCoordinate(coordinate):
                return False

        return True

    def validatePoint(self, geometry):
        numberOfCoordinates = len(geometry.coordinates)

        if numberOfCoordinates != 1:
            raise Exception
        
        for element in geometry.coordinates:
            try:
                self.validateCoordinate(element)
            except:
                self.logger.error(self.translations["err_validation"], [geometry.type, element.ptId], logToFile=True)
                self.errCount += 1

        return geometry

    def validateLineString(self, geometry):
        numberOfCoordinates = len(geometry.coordinates)

        if numberOfCoordinates < 2:
            raise Exception
        
        for element in geometry.coordinates:
            try:
                self.validateCoordinate(element)
            except:
                self.logger.error(self.translations["err_validation"], [geometry.type, element.ptId], logToFile=True)
                self.errCount += 1
                
        return geometry
    
    def validatePolygon(self, geometry):
        numberOfCoordinates = len(geometry.coordinates)

        if numberOfCoordinates < 3:
            raise Exception
        
        for element in geometry.coordinates:
            try:
                self.validateCoordinate(element)
            except:
                self.logger.error(self.translations["err_validation"], [geometry.type, element.ptId], logToFile=True)
                self.errCount += 1
        
        return geometry
        
    def validateMultiPoint(self, geometry):
        numberOfPoints = len(geometry.points)

        if numberOfPoints < 2:
            raise Exception
        
        for element in geometry.points:
            try:
                self.validatePoint(element)
            except:
                self.logger.error(self.translations["err_validation"], [element.type, element.ptId], logToFile=True)
                self.errCount += 1

        return geometry
        
    def validateMultiLineString(self, geometry):
        numberOfLineStrings = len(geometry.lineStrings)

        if numberOfLineStrings < 2:
            raise Exception
        
        for element in geometry.lineStrings:
            try:
                self.validateLineString(element)
            except:
                self.logger.error(self.translations["err_validation"], [element.type, element.ptId], logToFile=True)
                self.errCount += 1
        
        return geometry

    def validateMultiPolygon(self, geometry):
        numberOfPolygons = len(geometry.polygons)

        if numberOfPolygons < 3:
            raise Exception
        
        for element in geometry.polygons:
            try:
                self.validatePolygon(element)
            except:
                self.logger.error(self.translations["err_validation"], [element.type, element.ptId], logToFile=True)
                self.errCount += 1

        return geometry

    def validateGeometry(self, geometry):
        type = self.determineGeometryType(geometry)

        try:
            if type == OutputType.POINT:
                return self.validatePoint(geometry)
            elif type == OutputType.LINESTRING:
                return self.validateLineString(geometry)
            elif type == OutputType.POLYGON:
                return self.validatePolygon(geometry)
            elif type == OutputType.MULTI_POINT:
                return self.validateMultiPoint(geometry)
            elif type == OutputType.MULTI_LINESTRING:
                return self.validateMultiLineString(geometry)
            elif type == OutputType.MULTI_POLYGON:
                return self.validateMultiPolygon(geometry)
        except:
            raise Exception
        
    def validate(self, featureCollectionModel):
        validModel = FeatureCollection()

        for element in featureCollectionModel.features:
            try:
                validGeometry = self.validateGeometry(element.geometry)
                feature = Feature(element.identifier, validGeometry)
                validModel.addFeature(feature)
            except:
                self.logger.error(self.translations["err_validation_feature"], [element.identifier], logToFile=True)
        
        return validModel
