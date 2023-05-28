from geojson.featureCollection import FeatureCollection
from geojson.feature import Feature
from geojson.polygon import Polygon
from geojson.coordinate import Coordinate

class Modeller():

    def __init__(self):
        pass

    def createCoordinate(self, dictLine):
        east = str(dictLine['East']).replace(' ', ''),
        north = str(dictLine['North']).replace(' ', ''),
        height = str(dictLine['Height']).replace(' ', '')

        return Coordinate(east, north, height)

    def createGeometry(self, dict):
        geometry = Polygon()

        for dictLine in dict:
            coordinate = self.createCoordinate(dictLine)
            geometry.addCoordinate(coordinate)

        return geometry

    def createFeature(self, dict):
        geometry = self.createGeometry(dict)

        identifier = dict[0]['Attribut1']

        return Feature(identifier, geometry)

    def createFeatures(self, dicts):
        list = []

        for dict in dicts:
            feature = self.createFeature(dict)
            list.append(feature)
        
        return list

    def createFeatureCollection(self, dicts):
        featureList = self.createFeatures(dicts)

        return FeatureCollection(featureList)
    
    def convertInputToModel(self, dicts):
        return self.createFeatureCollection(dicts)
