import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
def from_root(*paths):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *paths)

#constants for log config
LOG_DIR = 'logs'
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
MAX_LOG_SIZE = 5 * 1024 * 1024 # 5MB
BACKUP_COUNT = 3

#CONSTRUCT LOG FILE PATH
log_file_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_file_path,exist_ok=True)
log_file_path = os.path.join(log_file_path, LOG_FILE)

def configure_logger():
    "Configures logging with a rotatingfilehandler & consolehandler "

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)


    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

configure_logger()