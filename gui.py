import PySimpleGUI as sg

from utils.util import Util

from enums.outputType import OutputType

class Gui():

    def __init__(self, programTitle, language):
        self.programTitle = programTitle
        self.util = Util()
        self.translations = self.util.loadTranslations(language)
        self.layout = self.createLayout()
        self.window = sg.Window(self.programTitle, self.layout)

    def createLayout(self):
        return [
                    [
                        sg.Text(self.translations["gui_header"])
                    ],
                    [
                        sg.Input(visible=True, enable_events=True, key='-INPUT-', size=(30,1)),
                        sg.FilesBrowse(self.translations["gui_browse"], file_types=(("CSV Files","*.csv"),))
                    ],
                    [
                        sg.DropDown(values=[], enable_events=True, key='-CODE-', disabled=True, size=(30,1))
                    ],
                    [
                        sg.Radio(OutputType.POLYGON.getTitleCase(), "GEOMTYPE", enable_events=True, default=True, key='-GEOM_POLYGON-')
                    ],
                    [
                        sg.Radio(OutputType.POINT.getTitleCase(), "GEOMTYPE", enable_events=True, default=False, key='-GEOM_POINT-')
                    ],
                    [
                        sg.Radio(OutputType.LINESTRING.getTitleCase(), "GEOMTYPE", enable_events=True, default=False, key='-GEOM_LINESTRING-')
                    ],
                    [
                        sg.Button(self.translations["gui_convert"], key="-CONVERT-", disabled=True)
                    ],
                    [
                        sg.Button(self.translations["gui_close"], key="-CLOSE-")
                    ]
                ]
    
    def enableElement(self, element):
        self.window[element].update(disabled=False)

    def disableElement(self, element):
        self.window[element].update(disabled=True)
    
    def updateValues(self, element, values):
        self.window[element].update(values=values)

    def readValues(self):
        return self.window.read()

    def destroy(self):
        self.window.close()

    def handleInput(self, values):
        self.selectedFileName = values['-INPUT-']
        self.logger.info("File chosen: " + self.selectedFileName)
        self.rows = self.inputReader.createCsvRowList(self.selectedFileName)

    def handleCode(self, values):
        selectedCode = values['-CODE-']
        self.logger.info("Code selected: " + selectedCode)
        self.filteredRows = self.inputReader.filterByCode(self.rows, selectedCode)

    def handleGui(self):
        
        while True:
            event, values = self.gui.readValues()

            if event == "-INPUT-":
                self.handleInput(values)

                entries = self.inputReader.createCodeDropDownEntries(self.rows)
                self.gui.updateValues("-CODE-", entries)
                self.gui.enableElement("-CODE-")

                self.gui.disableElement("-CONVERT-")

            if event == "-CODE-":
                self.handleCode(values)

                splitData = self.inputReader.splitByIdentifier(self.filteredRows)
                self.aggregatedData = self.inputReader.aggregateByIdentifier(splitData)

                self.gui.enableElement("-CONVERT-")
                self.logger.info(f"Found {str(len(splitData))} objects.")

            if event == "-GEOM_POINT-":
                self.selectedType = OutputType.POINT
                self.logger.info("Output-type selected: " + self.selectedType.value)

            if event == "-GEOM_LINESTRING-":
                self.selectedType = OutputType.LINESTRING
                self.logger.info("Output-type selected: " + self.selectedType.value)

            if event == "-GEOM_POLYGON-":
                self.selectedType = OutputType.POLYGON
                self.logger.info("Output-type selected: " + self.selectedType.value)

            if event == "-CONVERT-":
                featureCollectionModel = self.modeller.createFeatureCollection(self.aggregatedData, self.selectedType)
                self.logger.info("Converted to object-model.")
                
                output = str(featureCollectionModel)

                outputFileName = self.util.createOutputFileName(self.selectedFileName, self.selectedType, self.selectedFileType)
                self.writer.writeToFile(output, outputFileName)

            if event == "-CLOSE-" or event == sg.WIN_CLOSED:
                break

        self.gui.destroy()
