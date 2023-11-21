from csvGeom.enums.logtype import LogType
from csvGeom.utils.util import Util
from csvGeom.utils.fileWriter import FileWriter


class Logger:
    INFO_DEL = ">>>"
    DEBUG_DEL = "---"
    ERROR_DEL = "!!!"
    CRITICAL_DEL = "-X-"

    @staticmethod
    def info(msg, objects=None, log_to_file=False):
        if objects is None:
            objects = []
        Logger.print_msg(LogType.INFO.value, Logger.INFO_DEL, msg, objects, log_to_file)

    @staticmethod
    def debug(msg, objects=None, log_to_file=False):
        if objects is None:
            objects = []
        Logger.print_msg(LogType.DEBUG.value, Logger.DEBUG_DEL, msg, objects, log_to_file)

    @staticmethod
    def error(msg, objects=None, log_to_file=False):
        if objects is None:
            objects = []
        Logger.print_msg(LogType.ERR.value, Logger.ERROR_DEL, msg, objects, log_to_file)

    @staticmethod
    def critical(msg, objects=None, log_to_file=False):
        if objects is None:
            objects = []
        Logger.print_msg(LogType.CRIT.value, Logger.CRITICAL_DEL, msg, objects, log_to_file)

    @staticmethod
    def print_msg(log_type, delimiter, msg, objects=None, log_to_file=False):
        if objects is None:
            objects = []
        formatted_msg = Util.create_formatted_msg(msg, objects)
        print(log_type, delimiter, formatted_msg)

        if log_to_file:
            FileWriter.append_to_file(formatted_msg + "\n", "./log.txt")
