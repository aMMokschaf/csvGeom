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

    def createFeatureHeader(self, identifier, selectedType):
        util = self.util
        
        header = util.indent(2) + '{'
        header = header + util.indent(3) + '"type": "Feature",'
        header = header + util.indent(3) + '"properties": {'
        header = header + util.indent(4) + '"identifier": "' + identifier + '"'
        header = header + util.indent(3) + '},'
        header = header + util.indent(3) + '"geometry": {'
        header = header + util.indent(4) + '"type": "' + OutputType(selectedType).getTitleCase() + '",'

        return header

    def createFeatureFooter(self):
        util = self.util

        footer = ''
        footer = footer + util.indent(3) + '}'
        footer = footer + util.indent(2) + '}'

        return footer

    def createFeature(self, dict, selectedType):
        identifier = str(dict[0]['Attribut1'])

        header = self.createFeatureHeader(identifier, selectedType)

        if selectedType == "polygon":
            geometry = self.createPolygon(dict)
        elif selectedType == "point": 
            geometry = self.createPoint(dict)
        
        footer = self.createFeatureFooter()

        return header + geometry + footer

    def createPolygon(self, dict):
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

    
    def createPoint(self, dict):
        util = self.util

        # fixed index for test
        # Point should actually switch flexibly between point and multipoint
        # :(
        values = [
                        str(dict[0]['East']).replace(' ', ''),
                        str(dict[0]['North']).replace(' ', ''),
                        str(dict[0]['Height']).replace(' ', '')
                ]
        
        point = util.indent(4) + '"coordinates": '
        point = point + self.createSingleCoord(values, 4, True)

        return point
    
    def createLinestring(self):
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
        data = data + self.createFeature(dict, selectedType)
        data = data + self.createFeatureCollectionFooter()

        return data
