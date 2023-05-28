from enum import Enum
from util import Util

class LogType(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    ERR = "ERROR"
    CRIT = "CRITICAL"

class Logger():

    DELIMITER = ">>>"

    def __init__(self):
        pass

    def info(self, msg, objects=[]):
        self.printMsg(LogType.INFO.value, msg)
        if len(objects) > 0:
            for obj in objects:
                print(Util().indent(1), str(obj), '\n')

    def debug(self, msg):
        self.printMsg(LogType.DEBUG.value, msg)

    def error(self, msg):
        self.printMsg(LogType.ERR.value, msg)

    def critical(self, msg):
        self.printMsg(LogType.CRIT.value, msg)
    
    def printMsg(self, logType, msg):
        print(logType, self.DELIMITER, msg)