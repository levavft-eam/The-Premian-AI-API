import logging
import logging.config
from pathlib import Path, PurePath

import os
from datetime import datetime
from dotenv import find_dotenv, load_dotenv

# find .env file in parent directory
env_file = find_dotenv()
load_dotenv()

THIS_FOLDER = Path(__file__).parent.resolve()
BASE_DIR = THIS_FOLDER / '..' / '..'
CONFIG_DIR = BASE_DIR / 'config'
LOG_DIR = BASE_DIR / 'logs'


def setup_logging():
    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}
    config = log_configs.get(os.environ["ENV"], "logging.dev.ini")
    config_path = CONFIG_DIR / config

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    logfile_name = LOG_DIR / f'{timestamp}.log'

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": repr(str(logfile_name))[1:-1]},
    )


def test():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Test!")


if __name__ == "__main__":
    test()
