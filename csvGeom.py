import PySimpleGUI as sg

from gui import Gui
from inputReader import InputReader
from modeller import Modeller
from utils.util import Util
from utils.fileWriter import FileWriter
from enums.outputType import OutputType
from enums.fileType import FileType
from utils.logger import Logger
from outputFormatter import OutputFormatter

class Main():

    PROGRAM_TITLE = "csvGeom v0.2.0"

    def __init__(self):
        self.util = Util()
        self.writer = FileWriter()
        self.logger = Logger()
        self.modeller = Modeller()
        self.inputReader = InputReader()
        self.outputFormatter = OutputFormatter()

        self.dict = []
        self.filteredDict = []

        self.selectedFileName = None
        self.selectedType = OutputType.POLYGON
        self.selectedFileType = FileType.GEO_JSON

        self.featureCollectionModel = None

    def handleInput(self, values):
        self.selectedFileName = values['-INPUT-']
        self.logger.info("File chosen: " + self.selectedFileName)
        self.dict = self.inputReader.createDictionary(self.selectedFileName)

    def handleCode(self, values):
        selectedCode = values['-CODE-']
        self.logger.info("Code selected: " + selectedCode)
        self.filteredDict = self.inputReader.filterByCode(self.dict, selectedCode)
        
    def main(self):

        gui = Gui(self.PROGRAM_TITLE)
        window = gui.initializeGui()

        while True:
            event, values = window.read()

            if event == "-INPUT-":
                self.handleInput(values)

                list = self.inputReader.createDropDownList(self.dict)
                window["-CODE-"].update(values=list, disabled=False)

            if event == "-CODE-":
                self.handleCode(values)

                splitData = self.inputReader.splitByIdentifier(self.filteredDict)

                window["-CONVERT-"].update(disabled=False)
                self.logger.info(f"Found {str(len(splitData))} objects.", splitData)

            if event == "-GEOM_POINT-":
                self.selectedType = OutputType.POINT
                self.logger.info("Output-type selected: " + self.selectedType.value)

            if event == "-GEOM_POLYGON-":
                self.selectedType = OutputType.POLYGON
                self.logger.info("Output-type selected: " + self.selectedType.value)

            if event == "-CONVERT-":
                featureCollectionModel = self.modeller.createFeatureCollection(splitData, self.selectedType)
                self.logger.info("Converted to object-model.")

                data = self.outputFormatter.createFeatureCollection(featureCollectionModel)
                self.logger.info("Converted to GeoJSON.")

                outputFileName = self.util.createOutputFileName(self.selectedFileName, self.selectedType, self.selectedFileType)
                self.writer.writeToFile(data, outputFileName)

            if event == "-CLOSE-" or event == sg.WIN_CLOSED:
                break

        window.close()

if __name__ == '__main__':
    app = Main()
    app.main()
