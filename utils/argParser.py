import argparse

class ArgParser():

    def __init__(self):
        parser = argparse.ArgumentParser("Arguments:")

        parser.add_argument('--l', type=str, default="en", help="Language")
        
        self.args = parser.parse_args()
