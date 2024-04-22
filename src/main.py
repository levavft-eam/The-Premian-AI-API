import logging

from common.setup_logging import setup_logging
from stt.whisper import load_pipeline
from download.dlp import list_formats, download_video


logger = logging.getLogger(__name__)
setup_logging()


def main():
    video_id = "c8OwVTBdE6s"

    logger.info("Program started")
    # logger.info(download_video(video_id))
    # pipeline = load_pipeline()
    # logger.info(pipeline('data/c8OwVTBdE6s.webm'))

    logger.info("Program finished")


if __name__ == "__main__":
    main()

