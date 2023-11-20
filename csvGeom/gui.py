import PySimpleGUI as sG

from csvGeom.utils.util import Util

from csvGeom.enums.outputType import OutputType


class Gui:

    def __init__(self, program_title, language):
        self.programTitle = program_title
        self.translations = Util.load_translations(language)
        self.layout = self.create_layout()
        self.window = sG.Window(self.programTitle, self.layout)

    def create_layout(self):
        return [
                    [
                        sG.Text(self.translations["gui_header"])
                    ],
                    [
                        sG.Input(
                            visible=True,
                            enable_events=True,
                            key='-INPUT-',
                            size=(30, 1)
                        ),
                        sG.FilesBrowse(
                            self.translations["gui_browse"],
                            file_types=(("CSV Files", "*.csv"),)
                        )
                    ],
                    [
                        sG.DropDown(
                            values=[],
                            enable_events=True,
                            key='-CODE-',
                            disabled=True,
                            size=(30, 1)
                        )
                    ],
                    [
                        sG.Radio(
                            OutputType.POLYGON.get_title_case(),
                            "GEOMTYPE",
                            enable_events=True,
                            default=True,
                            key='-GEOM_POLYGON-')
                    ],
                    [
                        sG.Radio(
                            OutputType.POINT.get_title_case(),
                            "GEOMTYPE",
                            enable_events=True,
                            default=False,
                            key='-GEOM_POINT-'
                        )
                    ],
                    [
                        sG.Radio(
                            OutputType.LINESTRING.get_title_case(),
                            "GEOMTYPE",
                            enable_events=True,
                            default=False,
                            key='-GEOM_LINESTRING-'
                        )
                    ],
                    [
                        sG.Graph(
                            (700, 50),
                            (0, 0),
                            (700, 50),
                            background_color='white', key='errRectangle'
                        )
                    ],
                    [
                        sG.Button(
                            self.translations["gui_convert"],
                            key="-CONVERT-",
                            disabled=True
                        )
                    ],
                    [
                        sG.Button(
                            self.translations["gui_close"],
                            key="-CLOSE-"
                        )
                    ]
                ]
    
    def enable_element(self, element):
        self.window[element].update(disabled=False)

    def disable_element(self, element):
        self.window[element].update(disabled=True)
    
    def update_values(self, element, values):
        self.window[element].update(values=values)

    def read_values(self):
        return self.window.read()
    
    def reset_err_msg(self):
        self.window["errRectangle"].update(background_color='white')
        self.window["errRectangle"].erase()
    
    def update_err_msg(self, count):
        if count > 0:
            color = 'red'
            err_msg = self.translations["gui_error_validation"]
            formatted_msg = Util.create_formatted_msg(err_msg, [count])

            self.window["errRectangle"].draw_text(formatted_msg, (350, 25), color='black')
        else:
            color = "green"

        self.window["errRectangle"].update(background_color=color)

    def destroy(self):
        self.window.close()
