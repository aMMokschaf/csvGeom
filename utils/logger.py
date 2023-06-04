from enum import Enum
from utils.util import Util

class LogType(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    ERR = "ERROR"
    CRIT = "CRITICAL"

class Logger():

    INFO_DELIMITER = ">"
    DEBUG_DELIMITER = "-->"
    ERROR_DELIMITER = "!"
    CRITICAL_DELIMITER = "X"

    def __init__(self):
        pass

    def info(self, msg, objects=[]):
        self.printMsg(LogType.INFO.value, self.INFO_DELIMITER, msg)
        if len(objects) > 0:
            for obj in objects:
                print(Util().indent(1), str(obj), '\n')

    def debug(self, msg):
        self.printMsg(LogType.DEBUG.value, self.DEBUG_DELIMITER, msg)

    def error(self, msg):
        self.printMsg(LogType.ERR.value, self.ERROR_DELIMITER,msg)

    def critical(self, msg):
        self.printMsg(LogType.CRIT.value, self.CRITICAL_DELIMITER, msg)
    
    def printMsg(self, logType, delimiter, msg):
        print(logType, delimiter, msg)