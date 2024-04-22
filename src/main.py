import logging

from common.setup_logging import setup_logging
from stt.whisper import load_pipeline


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Program started")
    pipeline = load_pipeline()
    logger.info("Program finished")
