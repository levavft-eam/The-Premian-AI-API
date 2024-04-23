import logging
from datetime import datetime

from common.setup_logging import setup_logging
from stt.whisper import load_pipeline
from download.dlp import list_formats, download_video
from metadata.google_api import get_video_statistics
from categorize.chatgpt import get_text_category, TEST_STRING

logger = logging.getLogger(__name__)
setup_logging()


def test():
    video_id = "c8OwVTBdE6s"

    logger.info("Program started")
    # logger.info(download_video(video_id))
    # pipeline = load_pipeline()
    # logger.info(pipeline('data/c8OwVTBdE6s.webm'))
    # logger.info(get_video_statistics(video_id))
    # logger.info(get_text_category(TEST_STRING))
    logger.info("Program finished")


def main():
    logger.info("Program started")
    now = datetime.now()

    video_id = "c8OwVTBdE6s"
    audio_file_path = download_video(video_id, False)
    logger.info(audio_file_path)
    pipeline = load_pipeline()
    result = pipeline(audio_file_path, generate_kwargs={"language": "korean"})
    text = result["text"]
    logger.info(text)
    statistics = get_video_statistics(video_id)
    logger.info(statistics)
    category = get_text_category(text)
    logger.info(category)
    logger.info(f"Program finished. Duration: {datetime.now() - now}")


if __name__ == "__main__":
    main()

