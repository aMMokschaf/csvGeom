
TAB = '    ' # Four Spaces

class Util():
    def indent(self, n):
        indent = TAB * n
        indent = '\n' + indent
        return indent
    
    def getFileNameWithoutSuffix(self, filename):
        return filename.rsplit(".", 1)[0]
    
    #temporary method to debug the object-model
    def debugFeatureCollection(self, featureCollection):
        print(featureCollection)
        for feature in featureCollection.features:
            print(feature)
            geometry = feature.geometry
            for coord in geometry.coordinates:
                print(coord)

