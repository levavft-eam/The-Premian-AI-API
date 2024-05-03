import logging
from datetime import datetime

from common.setup_logging import setup_logging
from stt.whisper import test as test_whisper
from metadata.google_api import test as test_google_api
from src.flows import test, test2, test3

logger = logging.getLogger(__name__)
setup_logging()


def main():
    test_google_api()


if __name__ == '__main__':
    logger.info("Program started")
    now = datetime.now()
    main()
    logger.info(f"Program finished. Duration: {datetime.now() - now}")
