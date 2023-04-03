import logging

logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(threadName)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[stream_handler],
)
