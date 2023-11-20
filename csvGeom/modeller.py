from csvGeom.geojson.coordinate import Coordinate
from csvGeom.geojson.feature import Feature
from csvGeom.geojson.featureCollection import FeatureCollection

from csvGeom.geojson.point import Point
from csvGeom.geojson.lineString import LineString
from csvGeom.geojson.polygon import Polygon

from csvGeom.geojson.multipoint import Multipoint
from csvGeom.geojson.multiLineString import MultiLineString
from csvGeom.geojson.multiPolygon import MultiPolygon

from csvGeom.enums.outputType import OutputType

from csvGeom.utils.util import Util


class Modeller:

    def __init__(self, language, logger):
        self.util = Util()
        self.logger = logger
        self.translations = self.util.load_translations(language)

    def create_coordinate(self, row):
        pt_id = row.id.strip()
        east = row.east.strip()
        north = row.north.strip()
        height = row.height.strip()

        return Coordinate(pt_id, east, north, height)
    
    def create_point_geometry(self, row_list):
        coordinates = self.util.get_first_element(row_list)

        geometry = Point()
        row = self.util.get_first_element(coordinates)
        coordinate = self.create_coordinate(row)

        geometry.add_coordinate(coordinate)
        
        return geometry

    def create_line_string_geometry(self, row_list):
        coordinates = self.util.get_first_element(row_list)

        geometry = LineString()

        for rows in coordinates:
            coordinate = self.create_coordinate(rows)

            geometry.add_coordinate(coordinate)

        return geometry

    def create_polygon_geometry(self, row_list):
        coordinates = self.util.get_first_element(row_list)

        geometry = Polygon()

        for rows in coordinates:
            coordinate = self.create_coordinate(rows)

            geometry.add_coordinate(coordinate)

        return geometry

    def create_multi_point_geometry(self, row_list):
        geometry = Multipoint()

        for item in row_list:
            item_geometry = Point()

            for rows in item:
                coordinate = self.create_coordinate(rows)
                item_geometry.add_coordinate(coordinate)
                geometry.add_point(item_geometry)

        return geometry

    def create_multi_linestring_geometry(self, rowList):
        geometry = MultiLineString()

        for item in rowList:
            item_geometry = LineString()

            for rows in item:
                coordinate = self.create_coordinate(rows)
                item_geometry.add_coordinate(coordinate)
                geometry.add_line_string(item_geometry)

        return geometry

    def create_multi_polygon_geometry(self, row_list):
        geometry = MultiPolygon()
        for item in row_list:
            item_geometry = Polygon()

            for rows in item:
                coordinate = self.create_coordinate(rows)
                item_geometry.add_coordinate(coordinate)
                geometry.add_polygon(item_geometry)

        return geometry

    def create_geometry(self, row_list, selected_geometry_type):

        if selected_geometry_type == OutputType.POINT:
            return self.create_point_geometry(row_list)

        if selected_geometry_type == OutputType.LINESTRING:
            return self.create_line_string_geometry(row_list)

        if selected_geometry_type == OutputType.POLYGON:
            return self.create_polygon_geometry(row_list)

        if selected_geometry_type == OutputType.MULTI_POINT:
            return self.create_multi_point_geometry(row_list)

        if selected_geometry_type == OutputType.MULTI_LINESTRING:
            return self.create_multi_linestring_geometry(row_list)

        if selected_geometry_type == OutputType.MULTI_POLYGON:
            return self.create_multi_polygon_geometry(row_list)
        
    def switch_to_multi_geometry(self, selected_geometry_type):
        if selected_geometry_type == OutputType.POLYGON:
            return OutputType.MULTI_POLYGON

        elif selected_geometry_type == OutputType.LINESTRING:
            return OutputType.MULTI_LINESTRING

        elif selected_geometry_type == OutputType.POINT:
            return OutputType.MULTI_POINT
    
    def create_feature(self, row_list, selected_geometry_type):
        
        geometry = self.create_geometry(row_list, selected_geometry_type)
        if geometry is not None:
            first_coordinate_list = self.util.get_first_element(row_list)
            identifier = self.util.get_identifier_from_list(first_coordinate_list)
            return Feature(identifier, geometry)
        else:
            return None
        
    def transform_row_list_for_multi_point(self, rowList):
        list = []

        for subList in rowList:
            for coordinate in subList:
                list2 = [coordinate]
                list.append(list2)

        return list

    def create_features(self, rowLists, selectedGeometryType):
        list = []

        for rowList in rowLists:

            if selectedGeometryType == OutputType.POINT and len(rowList[0]) >= 2:

                geometry_type = self.switch_to_multi_geometry(selectedGeometryType)

                transformed_list = self.transform_row_list_for_multi_point(rowList)

                feature = self.create_feature(transformed_list, geometry_type)
                
            else:

                if len(rowList) >= 2:
                    geometry_type = self.switch_to_multi_geometry(selectedGeometryType)
                else:
                    geometry_type = selectedGeometryType

                feature = self.create_feature(rowList, geometry_type)

            if feature is not None:
                list.append(feature)
        
        return list

    def create_feature_collection(self, row_lists, selected_geometry_type):

        feature_list = self.create_features(row_lists, selected_geometry_type)

        feature_collection = FeatureCollection()

        feature_collection.features = feature_list

        return feature_collection
