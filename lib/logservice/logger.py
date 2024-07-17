import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
# from face import fileoperation
# pylint: disable=broad-except
def createdir(path):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, path)
    if not os.path.exists(final_directory):
     os.makedirs(final_directory)
    return

class Logger:
    cpath=os.getcwd()
    logpath=f"{cpath}/logs"
    createdir(logpath)
    fullpathfile=f"{logpath}/trace.log"
    rfh = logging.handlers.RotatingFileHandler(
    filename=fullpathfile, 
    mode='a',
    maxBytes=10*1024*1024,
    backupCount=10,
    encoding=None,
    delay=0
)

    # logging.basicConfig(filemode='a',filename=fullpathfile,filename="e:/trace.log",
    #                 format='%(asctime)s %(message)s',
    #                 filemode='w')
    # filename=fullpathfile,
    logging.basicConfig(level=logging.DEBUG,handlers=[rfh],
                    format='%(threadName)s: %(asctime)s - %(levelname)s- %(funcName)s(%(lineno)d)- %(message)s')
    
    def __init__(self, module=None):
        self.module = module
        log_level = os.environ.get("DEEPFACE_LOG_LEVEL", str(logging.INFO))
        try:
            self.log_level = int(log_level)
        except Exception as err:
            self.dump_log(
                f"Exception while parsing $DEEPFACE_LOG_LEVEL."
                f"Expected int but it is {log_level} ({str(err)})."
                "Setting app log level to info."
            )
            self.log_level = logging.INFO

    def info(self, message):
        if self.log_level <= logging.INFO:
            print(f"{message}")
            self.dump_log(f"{message}")

    def debug(self, message):
        if self.log_level <= logging.DEBUG:
            self.dump_log(f"🕷️ {message}")
            

    def warn(self, message):
        if self.log_level <= logging.WARNING:
            self.dump_log(f"⚠️ {message}")

    def error(self, message):
        if self.log_level <= logging.ERROR:
            self.dump_log(f"🔴 {message}")

    def critical(self, message):
        if self.log_level <= logging.CRITICAL:
            self.dump_log(f"💥 {message}")

    def dump_log(self, message):
        print(f"{str(datetime.now())[2:-7]} - {message}")


def get_singletonish_logger():
    # singleton design pattern
    global model_obj

    if not "model_obj" in globals():
        model_obj = {}

    if "logger" not in model_obj.keys():
        model_obj["logger"] = Logger(module="Singleton")
        
    # cpath=os.getcwd()
    # logpath=f"{cpath}/logs"
    # createdir(logpath)
    # fullpathfile=f"{logpath}/trace.log"
    # log_formatter = logging.Formatter('%(threadName)s: %(asctime)s - %(levelname)s %(funcName)s(%(lineno)d)- %(message)s')

# logFile = 'C:\\Temp\\log'


    # my_handler = RotatingFileHandler(fullpathfile, mode='a', maxBytes=5*1024*1024, 
    #                              backupCount=20, encoding=None, delay=0)
    # my_handler.setFormatter(log_formatter)
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger
