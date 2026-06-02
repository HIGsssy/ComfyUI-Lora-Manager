import logging
from aiohttp import web

from .base_model_routes import BaseModelRoutes
from .lora_routes import LoraRoutes
from ..services.anima_lora_service import AnimaLoraService
from ..services.service_registry import ServiceRegistry

logger = logging.getLogger(__name__)


class AnimaLoraRoutes(LoraRoutes):
    """Anima LoRA route controller.

    Inherits every LoRA route (including the hash-based CivitAI lookup and the
    LoRA-specific endpoints) but binds them under the ``anima_loras`` prefix and
    serves the dedicated Anima LoRAs page template.
    """

    def __init__(self):
        super().__init__()
        self.template_name = "anima_loras.html"

    async def initialize_services(self):
        """Initialize services from ServiceRegistry for the Anima LoRA scanner."""
        anima_lora_scanner = await ServiceRegistry.get_anima_lora_scanner()
        update_service = await ServiceRegistry.get_model_update_service()
        self.service = AnimaLoraService(
            anima_lora_scanner, update_service=update_service
        )
        self.set_model_update_service(update_service)

        # Attach service dependencies
        self.attach_service(self.service)

    def setup_routes(self, app: web.Application):
        """Setup Anima LoRA routes under the 'anima_loras' prefix."""
        # Schedule service initialization on app startup
        app.on_startup.append(lambda _: self.initialize_services())

        # Bypass LoraRoutes.setup_routes (which binds the 'loras' prefix) and
        # register the common + LoRA-specific routes under our own prefix.
        BaseModelRoutes.setup_routes(self, app, "anima_loras")
