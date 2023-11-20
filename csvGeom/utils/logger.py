from enum import Enum

from csvGeom.utils.util import Util


class LogType(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    ERR = "ERROR"
    CRIT = "CRITICAL"


class Logger:
    INFO_DEL = ">>>"
    DEBUG_DEL = "---"
    ERROR_DEL = "!!!"
    CRITICAL_DEL = "-X-"

    def __init__(self, writer):
        self.util = Util()
        self.writer = writer

    def info(self, msg, objects=[], log_to_file=False):
        self.print_msg(LogType.INFO.value, self.INFO_DEL, msg, objects, log_to_file)

    def debug(self, msg, objects=[], log_to_file=False):
        self.print_msg(LogType.DEBUG.value, self.DEBUG_DEL, msg, objects, log_to_file)

    def error(self, msg, objects=[], logToFile=False):
        self.print_msg(LogType.ERR.value, self.ERROR_DEL, msg, objects, logToFile)

    def critical(self, msg, objects=[], log_to_file=False):
        self.print_msg(LogType.CRIT.value, self.CRITICAL_DEL, msg, objects, log_to_file)

    def print_msg(self, logType, delimiter, msg, objects=[], log_to_file=False):
        formatted_msg = self.util.create_formatted_msg(msg, objects)
        print(logType, delimiter, formatted_msg)

        if self.writer is not None and log_to_file:
            self.writer.appendToFile(formatted_msg + "\n", "./log.txt")
