import logging

from src.common.setup_torch import device, torch_dtype
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

logger = logging.getLogger(__name__)


def load_pipeline():
    model_id = "openai/whisper-large-v3"
    logger.info(f"Initializing model: {model_id}")

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )
    return pipe


def test():
    logger.info("Starting whisper test")
    pipe = load_pipeline()
    result = pipe(f"../../data/c8OwVTBdE6s.webm", generate_kwargs={"language": "korean"})
    logger.info(result["text"])


if __name__ == '__main__':
    test()
