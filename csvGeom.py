# csvGeom v0.1.0

import PySimpleGUI as sg

from gui import Gui
from logic import Logic

class Main():

    PROGRAM_TITLE = "csvGeom v0.1.0"

    def main(self):
        gui = Gui(self.PROGRAM_TITLE)
        window = gui.initializeGui()

        logic = Logic()

        while True:
            event, values = window.read()

            if event == "Convert":
                logic.convertData(values)

            if event == "Close" or event == sg.WIN_CLOSED:
                break

        window.close()

if __name__ == '__main__':
    app = Main()
    app.main()
