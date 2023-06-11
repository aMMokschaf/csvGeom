from enum import Enum

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
        pass

    def indent(self, n):
        if n <= 0 or n > 10:
            self.error("Invalid number of requested indents.")
            return ""

        TAB = "    " # Four Spaces

        return TAB * n

    def info(self, msg, objects=[]):
        self.printMsg(LogType.INFO.value, self.INFO_DEL, msg)

        if len(objects) > 0:
            for index,obj in enumerate(objects):
                print(f"Object {index}:{self.indent(2)}{str(obj)}\n")

    def debug(self, msg):
        self.printMsg(LogType.DEBUG.value, self.DEBUG_DEL, msg)

    def error(self, msg):
        self.printMsg(LogType.ERR.value, self.ERROR_DEL, msg)

    def critical(self, msg):
        self.printMsg(LogType.CRIT.value, self.CRITICAL_DEL, msg)
    
    def printMsg(self, logType, delimiter, msg):
        print(logType, delimiter, msg)