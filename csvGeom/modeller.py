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

    @staticmethod
    def create_coordinate(row):
        pt_id = row.id.strip()
        east = row.east.strip()
        north = row.north.strip()
        height = row.height.strip()

        return Coordinate(pt_id, east, north, height)

    @staticmethod
    def create_point_geometry(row_list):
        coordinates = Util.get_first_element(row_list)

        geometry = Point()
        row = Util.get_first_element(coordinates)
        coordinate = Modeller.create_coordinate(row)

        geometry.add_coordinate(coordinate)
        
        return geometry

    @staticmethod
    def create_line_string_geometry(row_list):
        coordinates = Util.get_first_element(row_list)

        geometry = LineString()

        for rows in coordinates:
            coordinate = Modeller.create_coordinate(rows)

            geometry.add_coordinate(coordinate)

        return geometry

    @staticmethod
    def create_polygon_geometry(row_list):
        coordinates = Util.get_first_element(row_list)

        geometry = Polygon()

        for rows in coordinates:
            coordinate = Modeller.create_coordinate(rows)

            geometry.add_coordinate(coordinate)

        return geometry

    @staticmethod
    def create_multi_point_geometry(row_list):
        geometry = Multipoint()

        for item in row_list:
            item_geometry = Point()

            for rows in item:
                coordinate = Modeller.create_coordinate(rows)
                item_geometry.add_coordinate(coordinate)
                geometry.add_point(item_geometry)

        return geometry

    @staticmethod
    def create_multi_linestring_geometry(row_list):
        geometry = MultiLineString()

        for item in row_list:
            item_geometry = LineString()

            for rows in item:
                coordinate = Modeller.create_coordinate(rows)
                item_geometry.add_coordinate(coordinate)
                geometry.add_line_string(item_geometry)

        return geometry

    @staticmethod
    def create_multi_polygon_geometry(row_list):
        geometry = MultiPolygon()
        for item in row_list:
            item_geometry = Polygon()

            for rows in item:
                coordinate = Modeller.create_coordinate(rows)
                item_geometry.add_coordinate(coordinate)
                geometry.add_polygon(item_geometry)

        return geometry

    @staticmethod
    def create_geometry(row_list, selected_geometry_type):

        if selected_geometry_type == OutputType.POINT:
            return Modeller.create_point_geometry(row_list)

        if selected_geometry_type == OutputType.LINESTRING:
            return Modeller.create_line_string_geometry(row_list)

        if selected_geometry_type == OutputType.POLYGON:
            return Modeller.create_polygon_geometry(row_list)

        if selected_geometry_type == OutputType.MULTI_POINT:
            return Modeller.create_multi_point_geometry(row_list)

        if selected_geometry_type == OutputType.MULTI_LINESTRING:
            return Modeller.create_multi_linestring_geometry(row_list)

        if selected_geometry_type == OutputType.MULTI_POLYGON:
            return Modeller.create_multi_polygon_geometry(row_list)

    @staticmethod
    def switch_to_multi_geometry(selected_geometry_type):
        if selected_geometry_type == OutputType.POLYGON:
            return OutputType.MULTI_POLYGON

        elif selected_geometry_type == OutputType.LINESTRING:
            return OutputType.MULTI_LINESTRING

        elif selected_geometry_type == OutputType.POINT:
            return OutputType.MULTI_POINT

    @staticmethod
    def create_feature(row_list, selected_geometry_type):
        
        geometry = Modeller.create_geometry(row_list, selected_geometry_type)
        if geometry is not None:
            first_coordinate_list = Util.get_first_element(row_list)
            identifier = Util.get_identifier_from_list(first_coordinate_list)
            return Feature(identifier, geometry)
        else:
            return None

    @staticmethod
    def transform_row_list_for_multi_point(row_list):
        elements = []

        for subList in row_list:
            for coordinate in subList:
                element = [coordinate]
                elements.append(element)

        return elements

    @staticmethod
    def create_features(row_lists, selected_geometry_type):
        features = []

        for rowList in row_lists:

            if selected_geometry_type == OutputType.POINT and len(rowList[0]) >= 2:

                geometry_type = Modeller.switch_to_multi_geometry(selected_geometry_type)

                transformed_list = Modeller.transform_row_list_for_multi_point(rowList)

                feature = Modeller.create_feature(transformed_list, geometry_type)
                
            else:

                if len(rowList) >= 2:
                    geometry_type = Modeller.switch_to_multi_geometry(selected_geometry_type)
                else:
                    geometry_type = selected_geometry_type

                feature = Modeller.create_feature(rowList, geometry_type)

            if feature is not None:
                features.append(feature)
        
        return features

    @staticmethod
    def create_feature_collection(row_lists, selected_geometry_type):

        feature_list = Modeller.create_features(row_lists, selected_geometry_type)

        feature_collection = FeatureCollection()

        feature_collection.features = feature_list

        return feature_collection
