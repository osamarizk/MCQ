import logging
import os
from datetime import datetime

#define the file name (current date time with the below format and extension log)
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
#create in current directory folder called logs
log_path=os.path.join(os.getcwd(),"logs")
os.makedirs(log_path,exist_ok=True)

# set the full path of log dile
LOG_FILEPATH=os.path.join(log_path,LOG_FILE)

logging.basicConfig(level=logging.INFO,
        filename=LOG_FILEPATH,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
        )