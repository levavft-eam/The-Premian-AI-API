import logging

from common.setup_logging import setup_logging
from stt.whisper import load_pipeline
from download.dlp import list_formats, download_video
from metadata.google_api import get_video_statistics
from categorize.chatgpt import get_text_category, TEST_STRING

logger = logging.getLogger(__name__)
setup_logging()


def main():
    video_id = "c8OwVTBdE6s"

    logger.info("Program started")
    # logger.info(download_video(video_id))
    # pipeline = load_pipeline()
    # logger.info(pipeline('data/c8OwVTBdE6s.webm'))
    # logger.info(get_video_statistics(video_id))
    logger.info(get_text_category(TEST_STRING))
    logger.info("Program finished")


if __name__ == "__main__":
    main()

