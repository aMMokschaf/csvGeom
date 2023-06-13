from enum import Enum

from csvGeom.utils.util import Util

class LogType(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    ERR = "ERROR"
    CRIT = "CRITICAL"

class Logger():

    INFO_DEL = ">>>"
    DEBUG_DEL = "---"
    ERROR_DEL = "!!!"
    CRITICAL_DEL = "-X-"

    def __init__(self, writer):
        self.util = Util()
        self.writer = writer

    def info(self, msg, objects=[], logToFile=False):
        self.printMsg(LogType.INFO.value, self.INFO_DEL, msg, objects, logToFile)

    def debug(self, msg, objects=[], logToFile=False):
        self.printMsg(LogType.DEBUG.value, self.DEBUG_DEL, msg, objects, logToFile)

    def error(self, msg, objects=[], logToFile=False):
        self.printMsg(LogType.ERR.value, self.ERROR_DEL, msg, objects, logToFile)

    def critical(self, msg, objects=[], logToFile=False):
        self.printMsg(LogType.CRIT.value, self.CRITICAL_DEL, msg, objects, logToFile)
    
    def printMsg(self, logType, delimiter, msg, objects=[], logToFile=False):
        formattedMsg = self.util.createFormattedMsg(msg, objects)
        print(logType, delimiter, formattedMsg)

        if not self.writer == None and logToFile:
            self.writer.appendToFile(formattedMsg + "\n", "./log.txt")