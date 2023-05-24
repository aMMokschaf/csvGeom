
TAB = '    ' # Four Spaces

class Util():
    def indent(self, n):
        indent = TAB * n
        indent = '\n' + indent
        return indent
    
    def getFileNameWithoutSuffix(self, filename):
        return filename.rsplit(".", 1)[0]
    