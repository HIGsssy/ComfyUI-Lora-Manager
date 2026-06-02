import logging
from typing import List

from ..utils.models import LoraMetadata
from ..config import config
from .model_scanner import ModelScanner
from .model_hash_index import ModelHashIndex

logger = logging.getLogger(__name__)


class AnimaLoraScanner(ModelScanner):
    """Service for scanning and managing Anima LoRA files.

    Anima LoRAs are a distinct category that shares LoRA file handling and
    metadata behavior but is stored under its own model root
    (``<ComfyUI>/models/anima_loras``) and persisted under its own model type.
    """

    def __init__(self):
        # Anima LoRAs share the LoRA file extension set.
        file_extensions = {'.safetensors'}

        super().__init__(
            model_type="anima_loras",
            model_class=LoraMetadata,
            file_extensions=file_extensions,
            hash_index=ModelHashIndex(),
        )

    def get_model_roots(self) -> List[str]:
        """Get Anima LoRA root directories (including extra paths)"""
        roots: List[str] = []
        roots.extend(config.anima_loras_roots or [])
        roots.extend(config.extra_anima_loras_roots or [])
        # Remove duplicates while preserving order
        seen: set = set()
        unique_roots: List[str] = []
        for root in roots:
            if root and root not in seen:
                seen.add(root)
                unique_roots.append(root)
        return unique_roots
