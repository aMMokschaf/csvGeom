class FeatureCollection():

    type = "FeatureCollection"
    name = "csvGeom-Export"

    def __init__(self, features):
        self.features = features

    def __str__(self):
        start = '{"type": "FeatureCollection", "features":'
        end = '}'

        return f'{start}{self.features}{end}'
    
    def __repr__(self):
        return str(self)

    def __dict__(self):
        return {
            'type': 'FeatureCollection',
            'features': self.features
        }