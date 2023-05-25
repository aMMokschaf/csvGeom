from util import Util
from outputType import OutputType

class Converter():

    util = None

    def __init__(self):
        self.util = Util()

    def createSingleCoord(self, values, minIndent, last):
        util = self.util

        point = util.indent(minIndent) + '['
        point = point + util.indent(minIndent + 1) + values[0] + ','
        point = point + util.indent(minIndent + 1) + values[1] + ','
        point = point + util.indent(minIndent + 1) + values[2] + ''
        point = point + util.indent(minIndent) + ']'
        if last == False: 
            point = point + ','
        
        return point

    def createFeatureHeader(self, identifier, selectedType, multi):
        util = self.util
        
        header = util.indent(2) + '{'
        header = header + util.indent(3) + '"type": "Feature",'
        header = header + util.indent(3) + '"properties": {'
        header = header + util.indent(4) + '"identifier": "' + identifier + '"'
        header = header + util.indent(3) + '},'
        header = header + util.indent(3) + '"geometry": {'

        geometryType = OutputType(selectedType).getTitleCase()
        if multi == True:
            geometryType = "Multi" + geometryType

        header = header + util.indent(4) + '"type": "' + geometryType + '",'

        return header

    def createFeatureFooter(self):
        util = self.util

        footer = ''
        footer = footer + util.indent(3) + '}'
        footer = footer + util.indent(2) + '}'

        return footer

    def createFeature(self, dict, selectedType, multi):
        identifier = str(dict[0]['Attribut1'])

        header = self.createFeatureHeader(identifier, selectedType, multi)

        if selectedType == "polygon":
            coords = self.createPolygonCoords(dict)
        elif selectedType == "point": 
            coords = self.createPointCoords(dict)
        else:
            coords = False
        
        footer = self.createFeatureFooter()

        return header + coords + footer

    def createPolygonCoords(self, dict):
        util = self.util
        dictLength = len(dict)

        polygon = util.indent(4) + '"coordinates": ['
        polygon = polygon + util.indent(5) + '['

        for i in range(dictLength):
            values = [
                        str(dict[i]['East']).replace(' ', ''),
                        str(dict[i]['North']).replace(' ', ''),
                        str(dict[i]['Height']).replace(' ', '')
                    ]
            
            if i+1 == dictLength:
                polygon = polygon + self.createSingleCoord(values, 6, True)
            else:
                polygon = polygon + self.createSingleCoord(values, 6, False)
        
        polygon = polygon + util.indent(5) + ']'
        polygon = polygon + util.indent(4) + ']'

        return polygon

    
    def createPointCoords(self, dict):
        util = self.util

        point = util.indent(4) + '"coordinates": '

        dictLength = len(dict)
        if dictLength > 1:
            point = point + '\n' + util.indent(4) + '['

        for i in range(dictLength):
            values = [
                str(dict[i]['East']).replace(' ', ''),
                str(dict[i]['North']).replace(' ', ''),
                str(dict[i]['Height']).replace(' ', '')
                ]
            
            if i+1 == dictLength:
                point = point + self.createSingleCoord(values, 5, True)
            else:
                point = point + self.createSingleCoord(values, 5, False)

        if dictLength > 1:
            point = point + '\n' + util.indent(4) + ']'        
        
        return point
    
    def createLinestringCoords(self):
        pass

    def createFeatureCollectionHeader(self):
        util = self.util

        header = '{'
        header = header + util.indent(1) + '"type": "FeatureCollection",' 
        header = header + util.indent(1) + '"name": "csvGeom-Export",'
        header = header + util.indent(1) + '"features": [ '

        return header
    
    def createFeatureCollectionFooter(self):
        return self.util.indent(1) + ']' + '\n}'
    
    def createFeatureCollection(self, dict, selectedType):
        data = self.createFeatureCollectionHeader()
        
        identifiers = []

        for obj in dict:
            if obj['Attribut1'] not in identifiers:
                identifiers.append(obj['Attribut1'])

        for id in identifiers:
            new_dict = []
            for obj in dict:
                if obj['Attribut1'] == id:
                    new_dict.append(obj)
            if selectedType == "point" and len(new_dict) > 1:
                multi = True
            else:
                multi = False
            data = data + self.createFeature(new_dict, selectedType, multi)
            if id != identifiers[-1]:
                data = data + ','

        data = data + self.createFeatureCollectionFooter()

        return data
