from util import Util

class Converter():

    util = None

    def __init__(self):
        self.util = Util()

    def createPoint(self, values, minIndent, last):
        util = self.util

        point = util.indent(minIndent) + '['
        point = point + util.indent(minIndent + 1) + values[0] + ','
        point = point + util.indent(minIndent + 1) + values[1] + ','
        point = point + util.indent(minIndent + 1) + values[2] + ''
        point = point + util.indent(minIndent) + ']'
        if last == False: 
            point = point + ','
        
        return point
    
    def createPointFeature(self):
        pass
    
    def createLineFeature(self):
        pass

    def createFeatureHeader(self, identifier, geomType):
        util = self.util
        
        header = util.indent(2) + '{'
        header = header + util.indent(3) + '"type": "Feature",'
        header = header + util.indent(3) + '"properties": {'
        header = header + util.indent(4) + '"identifier": "' + identifier + '"'
        header = header + util.indent(3) + '},'
        header = header + util.indent(3) + '"geometry": {'
        header = header + util.indent(4) + '"type": "' + geomType + '",'
        header = header + util.indent(4) + '"coordinates": ['
        header = header + util.indent(5) + '['

        return header

    def createFeatureFooter(self):
        util = self.util

        footer = util.indent(5) + ']'
        footer = footer+ util.indent(4) + ']'
        
        footer = footer + util.indent(3) + '}'
        footer = footer + util.indent(2) + '}'

        return footer

    def createFeature(self, dict, geomType):
        identifier = str(dict[0]['Attribut1'])

        header = self.createFeatureHeader(identifier, geomType)

        if geomType == "Polygon":
            geometry = self.createPolygon(dict)
        else: 
            geometry = self.createPolygon(dict)
        
        footer = self.createFeatureFooter()

        return header + geometry + footer

    def createPolygon(self, dict):
        dictLength = len(dict)

        polygon = ''

        for i in range(dictLength):
            values = [
                        str(dict[i]['East']).replace(' ', ''),
                        str(dict[i]['North']).replace(' ', ''),
                        str(dict[i]['Height']).replace(' ', '')
                    ]
            
            if i+1 == dictLength:
                polygon = polygon + self.createPoint(values, 6, True)
            else:
                polygon = polygon + self.createPoint(values, 6, False)
        
        return polygon


    def createFeatureCollectionHeader(self):
        util = self.util

        header = '{'
        header = header + util.indent(1) + '"type": "FeatureCollection",' 
        header = header + util.indent(1) + '"name": "csvGeom-Export",'
        header = header + util.indent(1) + '"features": [ '

        return header
    
    def createFeatureCollectionFooter(self):
        return self.util.indent(1) + ']' + '\n}'
    
    def createFeatureCollection(self, dict, geomType):
        data = self.createFeatureCollectionHeader()
        data = data + self.createFeature(dict, geomType)
        data = data + self.createFeatureCollectionFooter()

        return data
