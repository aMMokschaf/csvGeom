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

    def __init__(self):
        self.util = Util()

    def info(self, msg, objects=[]):
        self.printMsg(LogType.INFO.value, self.INFO_DEL, msg, objects)

    def debug(self, msg, objects=[]):
        self.printMsg(LogType.DEBUG.value, self.DEBUG_DEL, msg, objects)

    def error(self, msg, objects=[]):
        self.printMsg(LogType.ERR.value, self.ERROR_DEL, msg, objects)

    def critical(self, msg, objects=[]):
        self.printMsg(LogType.CRIT.value, self.CRITICAL_DEL, msg, objects)
    
    def printMsg(self, logType, delimiter, msg, objects=[]):
        formattedMsg = self.util.createFormattedMsg(msg, objects)
        print(logType, delimiter, formattedMsg)