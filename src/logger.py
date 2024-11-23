import os
from pathlib import Path
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Create a console handler and set its formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

try:
    os.mkdir(Path(".") / "logs")
except FileExistsError:
    pass

# Create a file handler and set its formatter
file_handler = logging.FileHandler(
    Path(".") / "logs" / "redis-kicks.log"
)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("****************************************************")
logger.info("****************  Program Started!  ****************")
logger.info("**************** Logger configured! ****************")
logger.info("****************************************************")
