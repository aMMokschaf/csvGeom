import io

from csvGeom.utils.util import Util


class FileWriter:

    @staticmethod
    def write(data, filename, mode):
        try:
            file = io.open(filename, mode)
            file.write(data)
            file.close()
        except:
            raise Exception

    @staticmethod
    def write_to_file(data, filename):
        try:
            FileWriter.write(data, filename, "w")
        except:
            raise Exception

    @staticmethod
    def append_to_file(data, filename):
        try:
            FileWriter.write(data, filename, "a")
        except:
            raise Exception
        