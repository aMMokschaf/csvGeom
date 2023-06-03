class Feature():

    type = "Feature"

    def __init__(self, identifier, geometry):
        self.identifier = identifier
        self.geometry = geometry

    def __str__(self):
        start = '{"type": "Feature", "properties": { "identifier": "' + self.identifier + '"}, "geometry": {'
        end = '}}'

        return f'{start}{self.geometry}{end}'

    def __repr__(self):
        return str(self)
    
    def __dict__(self):
        return {
            'type': "Feature",
            'properties': {
                'identifier': self.identifier
            },
            'geometry': self.geometry
        }
