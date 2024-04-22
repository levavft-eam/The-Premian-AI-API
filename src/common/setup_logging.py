import logging
import logging.config

import os
from datetime import datetime
from dotenv import find_dotenv, load_dotenv

# find .env file in parent directory
env_file = find_dotenv()
load_dotenv()

BASE_DIR = ".."
if __name__ == "__main__":
    BASE_DIR += "/.."

CONFIG_DIR = f"{BASE_DIR}/config"
LOG_DIR = f"{BASE_DIR}/logs"


def setup_logging():
    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}
    config = log_configs.get(os.environ["ENV"], "logging.dev.ini")
    config_path = "/".join([CONFIG_DIR, config])

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"},
    )


def test():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Test!")


if __name__ == "__main__":
    test()
