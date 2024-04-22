import torch
import logging

logger = logging.getLogger(__name__)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
logger.info(f"Using device: {device} for torch.")
