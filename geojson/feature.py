class Feature():

    type = "Feature"

    def __init__(self, identifier, geometry):
        self.identifier = identifier
        self.geometry = geometry

    def __str__(self):
        return f"'identifier' : {self.identifier} 'geometry' : {self.geometry}"

    def __repr__(self):
        return str(self)
    
    def __dict__(self):
        return {
            'type' : "Feature",
            'properties': {
                'identifier': self.identifier
            },
            'geometry': self.geometry
        }
