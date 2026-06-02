import logging

from .base_model_service import BaseModelService
from .lora_service import LoraService
from ..utils.models import LoraMetadata

logger = logging.getLogger(__name__)


class AnimaLoraService(LoraService):
    """Anima LoRA service implementation.

    Reuses all LoRA business logic (formatting, filtering, letter counts,
    randomizer/cycler, trigger words) but registers under the distinct
    ``anima_loras`` model type so its cache stays isolated from regular LoRAs.
    """

    def __init__(self, scanner, update_service=None):
        # Bypass ``LoraService.__init__`` (which hardcodes the "lora" model type)
        # and initialize the base service with the Anima LoRA model type.
        BaseModelService.__init__(
            self,
            "anima_loras",
            scanner,
            LoraMetadata,
            update_service=update_service,
        )
