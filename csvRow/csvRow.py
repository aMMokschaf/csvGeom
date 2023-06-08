class CsvRow():

    def __init__(self):
        self.east = 0
        self.north = 0
        self.height = 0

        self.id = ""
        self.code = ""
        self.identifier = ""

    def __str__(self):
        return f"[{self.id}:{self.east},{self.north},{self.height}, identifier: {self.identifier}, code: {self.code}]"

    def __repr__(self):
        return str(self)
