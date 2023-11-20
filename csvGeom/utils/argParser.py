import argparse


class ArgParser:

    def __init__(self):
        parser = argparse.ArgumentParser("Arguments:")

        parser.add_argument('--l', type=str, default="en", help="Language")
        parser.add_argument('--cli', action="store_true", help="Disable GUI")
        parser.add_argument('--i', type=str, help="Path of input file")
        parser.add_argument('--o', type=str, help="Path of output file")
        parser.add_argument('--g', type=str, help="Geometry-type")

        self.args = parser.parse_args()
