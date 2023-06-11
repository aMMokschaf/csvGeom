class CsvRow():

    def __init__(self):
        self.east = ""
        self.north = ""
        self.height = ""

        self.id = ""
        self.code = ""
        self.identifier = ""

    def __str__(self):
        return f"[{self.id}:{self.east},{self.north},{self.height}, identifier: {self.identifier}, code: {self.code}]"

    def __repr__(self):
        return str(self)
