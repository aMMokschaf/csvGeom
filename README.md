# csvGeom
Convert Lists of Coordinates to a GeoJSON-FeatureCollection that can be imported to Field Desktop

This is a Python script that converts csv-Lists of coordinates and attributes to [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON)-files. The chosen file will be saved as "*filename*_*geometryType*.geojson" in the same place as the original file. The resulting file can be imported into any [iDAI.field / Field Desktop](https://github.com/dainst/idai-field) database project, provided the identifiers for each object already exist in the database. Alternatively, the contents of each features Geometry can be copied into the "Geometry"-Field of a Resource in Field Desktop. This way, exports from total stations can be seamlessly transferred to the database.

As of version 0.5.2 the following geometry-types are available:

- Point/MultiPoint
- LineString/MultiLineString
- Polygon/MultiPolygon

## Usage
Install dependencies by running
```
pip install -r requirements.txt
```

### Usage with GUI
Simply run
```
python3 csvGeom.py
```

### Usage with CLI
csvGeom supports several commandline-arguments:

- --l: Specify a custom translation-file you may have written.
- --cli: This switch turns on the cli-mode and disables the GUI.
- --i: Specify the complete path to the input-file, e.g. './examples/alster_testpolygon.csv'.
- --o: Specify the complete path and filename to the output-file. You don't need to type the .geojson-file-ending.
- --g: The geometry-type: 'Point', 'LineString' or 'Polygon'. If you don't specify a type or the type can't be parsed, it will revert to 'Polygon' as a default.

### Using csvGeom to import geometries into Field Desktop

You have to select the data according to the value in the *Code*-column, and choose the type of geometry that should be returned for your selection. Each different value in the *Identifier* column corresponds to one feature in the resulting FeatureCollection. When choosing Point, multiple rows with the same *Identifier* will be converted to MultiPoint. When choosing Polygon or LineString, consecutive rows with the same *Identifier* will be treated as one Polygon/Linestring. If the file contains multiple non-consecutive stretches of coordinates with the same *Identifier* separated by rows with different *Identifier*s, these will be treated as a MultiPolygon or MultiLineString of the same Feature. Thus, each *Identifier* corresponds to one Feature.

The GeoJSON-file can be imported into Field Desktop with 'Tools' > 'Import'. The *Identifiers* have to exist in the project database you want to import the file to, and their resources will be automatically updated with the corresponding geometry from the GeoJSON-file.

Alternatively, you can copy and paste the contents of each Features *coordinates* under *geometry* manually into the corresponding field in each form in Field Desktop.

## Format of the csv-File
Currently, the format of the csv-File **has** to have at least these column-headers (in any order, case-sensitive): "PtID,East,North,Code,Identifier" in the first row, and corresponding coordinates and data in the rows below (see examples). The decimal separator is "**.**". Optionally, you can specify the height value. For example, the csv-File may look like this: 

| PtID    |               East |              North | Height |    Code | Identifier|
|---------|-------------------:|-------------------:|-------:|--------:|----------:|
| TE33_01 | 10.000765844571617 | 53.564714308986836 |      0 | Polygon | Attribut1 |
| TE33_02 | 10.003275866953757 | 53.566722326892553 |      0 | Polygon | Attribut1 |
| TE33_03 | 10.003777871430186 | 53.571575036831355 |      0 | Polygon | Attribut1 |
| TE33_04 | 10.003108532128282 | 53.575256402991826 |      0 | Polygon | Attribut1 |
| TE33_05 | 10.000765844571617 |  53.57877043432682 |      0 | Polygon | Attribut1 |
| TE33_06 | 10.002439192826378 | 53.578435764675866 |      0 | Polygon | Attribut1 |
| TE33_07 | 10.004949215208518 | 53.575256402991826 |      0 | Polygon | Attribut1 |
| TE33_08 | 10.006957233114228 | 53.572077041307779 |      0 | Polygon | Attribut1 |
| TE33_09 | 10.008965251019941 | 53.569567018925639 |      0 | Polygon | Attribut1 |
| TE33_10 | 10.011977277878508 | 53.568228340321831 |      0 | Polygon | Attribut1 |
| TE33_11 |  10.01398529578422 | 53.566220322416122 |      0 | Polygon | Attribut1 |
| TE33_12 | 10.013315956482316 | 53.563040960732081 |      0 | Polygon | Attribut1 |
| TE33_13 | 10.008630581368989 | 53.560028933873511 |      0 | Polygon | Attribut1 |
| TE33_14 | 10.000933179397094 | 53.558188250793272 |      0 | Polygon | Attribut1 |
| TE33_15 |  9.998255822189478 | 53.559024924920656 |      0 | Polygon | Attribut1 |
| TE33_16 |  9.998925161491382 | 53.562204286604697 |      0 | Polygon | Attribut1 |
| TE33_17 | 10.000765844571617 | 53.564714308986836 |      0 | Polygon | Attribut1 |

### Output

The resulting GeoJSON-file will contain this: 

```
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "identifier": "Attribut1"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.000765844571617,
                            53.564714308986836,
                            0
                        ],
                        [
                            10.003275866953757,
                            53.566722326892553,
                            0
                        ],
                        [
                            10.003777871430186,
                            53.571575036831355,
                            0
                        ],
                        [
                            10.003108532128282,
                            53.575256402991826,
                            0
                        ],
                        [
                            10.000765844571617,
                            53.57877043432682,
                            0
                        ],
                        [
                            10.002439192826378,
                            53.578435764675866,
                            0
                        ],
                        [
                            10.004949215208518,
                            53.575256402991826,
                            0
                        ],
                        [
                            10.006957233114228,
                            53.572077041307779,
                            0
                        ],
                        [
                            10.008965251019941,
                            53.569567018925639,
                            0
                        ],
                        [
                            10.011977277878508,
                            53.568228340321831,
                            0
                        ],
                        [
                            10.01398529578422,
                            53.566220322416122,
                            0
                        ],
                        [
                            10.013315956482316,
                            53.563040960732081,
                            0
                        ],
                        [
                            10.008630581368989,
                            53.560028933873511,
                            0
                        ],
                        [
                            10.000933179397094,
                            53.558188250793272,
                            0
                        ],
                        [
                            9.998255822189478,
                            53.559024924920656,
                            0
                        ],
                        [
                            9.998925161491382,
                            53.562204286604697,
                            0
                        ],
                        [
                            10.000765844571617,
                            53.564714308986836,
                            0
                        ]
                    ]
                ]
            }
        }
    ]
}
```

And look like this on a map:

```geojson
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "identifier": "Attribut1"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.000765844571617,
                            53.564714308986836,
                            0
                        ],
                        [
                            10.003275866953757,
                            53.566722326892553,
                            0
                        ],
                        [
                            10.003777871430186,
                            53.571575036831355,
                            0
                        ],
                        [
                            10.003108532128282,
                            53.575256402991826,
                            0
                        ],
                        [
                            10.000765844571617,
                            53.57877043432682,
                            0
                        ],
                        [
                            10.002439192826378,
                            53.578435764675866,
                            0
                        ],
                        [
                            10.004949215208518,
                            53.575256402991826,
                            0
                        ],
                        [
                            10.006957233114228,
                            53.572077041307779,
                            0
                        ],
                        [
                            10.008965251019941,
                            53.569567018925639,
                            0
                        ],
                        [
                            10.011977277878508,
                            53.568228340321831,
                            0
                        ],
                        [
                            10.01398529578422,
                            53.566220322416122,
                            0
                        ],
                        [
                            10.013315956482316,
                            53.563040960732081,
                            0
                        ],
                        [
                            10.008630581368989,
                            53.560028933873511,
                            0
                        ],
                        [
                            10.000933179397094,
                            53.558188250793272,
                            0
                        ],
                        [
                            9.998255822189478,
                            53.559024924920656,
                            0
                        ],
                        [
                            9.998925161491382,
                            53.562204286604697,
                            0
                        ],
                        [
                            10.000765844571617,
                            53.564714308986836,
                            0
                        ]
                    ]
                ]
            }
        }
    ]
}
```

## Context
The first version of this script was produced during @lsteinmann-s work for the [Miletus Excavation](https://www.miletgrabung.uni-hamburg.de/) in the course of the DFG/ANR-funded project ["Life Forms in the Megapolis: Miletus in the Longue Durée"](https://www.kulturwissenschaften.uni-hamburg.de/ka/forschung/lebensformen-megapolis.html). This tool has since been significantly updated and developed by @lsteinmann and @msingr.
