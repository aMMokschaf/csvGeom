import io

class FileWriter():

    def __init__(self):
        pass

    def writeToFile(self, data, filename):
        file = io.open(filename, "w")
        file.write(data)
        file.close()
