# csvGeom v0.1.0

import PySimpleGUI as sg

from gui import Gui
from logic import Logic
from util import Util
from converter import Converter
from fileWriter import FileWriter

class Main():

    PROGRAM_TITLE = "csvGeom v0.1.0"
    dict = []

    def __init__(self):
        self.util = Util()
        self.converter = Converter()
        self.writer = FileWriter()

    def main(self):

        gui = Gui(self.PROGRAM_TITLE)
        window = gui.initializeGui()

        logic = Logic()

        while True:
            event, values = window.read()

            if event == "-IN-":
                inputFileName = values['-IN-']
                self.dict = logic.createDictionary(inputFileName)
                # logic.filterCodes() implement this
                # How to activate the dropdown for code-selection?

            if event == "CodeSelected":
                pass
                # dict wird nach dem selektierten Code gefiltert.
                # Wenn File und Code selected sind wird der Convert-Button erst aktiviert.

            if event == "Convert":
                inputFileName = values['-IN-']
                outputFileName = self.util.getFileNameWithoutSuffix(inputFileName)
                outputFileName = outputFileName + '.geojson' #+ type + fileType

                data = logic.convertData(self.dict)

                self.writer.writeToFile(data, outputFileName)

            if event == "Close" or event == sg.WIN_CLOSED:
                break

        window.close()

if __name__ == '__main__':
    app = Main()
    app.main()
