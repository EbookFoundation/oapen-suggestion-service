import logging

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("debug.log")
file_handler.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(threadName)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[file_handler],
)
