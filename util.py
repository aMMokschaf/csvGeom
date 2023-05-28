
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
        print("fc type: ", featureCollection.type)
        print("fc name: ", featureCollection.name)
        print("fc features")
        for feature in featureCollection.features:
            print("identifier:", feature.identifier)
            print("geometry: ")
            geometry = feature.geometry
            for coord in geometry.coordinates:
                print("east: ", coord.east)
                print("north: ", coord.north)
                print("height: ", coord.height)
                print("----")
