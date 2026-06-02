"""Tests for the Anima LoRA model category registration and scanner."""

from __future__ import annotations

import pytest


def test_register_default_model_types_includes_anima_loras():
    """``register_default_model_types`` should register the Anima LoRA category."""

    from py.services.model_service_factory import (
        ModelServiceFactory,
        register_default_model_types,
    )
    from py.services.anima_lora_service import AnimaLoraService
    from py.routes.anima_lora_routes import AnimaLoraRoutes

    ModelServiceFactory.clear_registrations()
    try:
        register_default_model_types()

        assert ModelServiceFactory.is_registered("anima_loras")
        assert ModelServiceFactory.get_service_class("anima_loras") is AnimaLoraService
        assert ModelServiceFactory.get_route_class("anima_loras") is AnimaLoraRoutes

        # Existing categories must remain registered.
        for model_type in ("lora", "checkpoint", "embedding"):
            assert ModelServiceFactory.is_registered(model_type)
    finally:
        ModelServiceFactory.clear_registrations()


@pytest.mark.asyncio
async def test_anima_lora_scanner_uses_anima_roots(monkeypatch):
    """The Anima scanner reads its own roots and shares LoRA file extensions."""

    from py.config import config
    from py.services.anima_lora_scanner import AnimaLoraScanner

    monkeypatch.setattr(config, "anima_loras_roots", ["/models/anima_loras"], raising=False)
    monkeypatch.setattr(
        config, "extra_anima_loras_roots", ["/extra/anima_loras"], raising=False
    )

    scanner = await AnimaLoraScanner.get_instance()

    assert scanner.model_type == "anima_loras"
    assert scanner.file_extensions == {".safetensors"}

    roots = scanner.get_model_roots()
    assert "/models/anima_loras" in roots
    assert "/extra/anima_loras" in roots


@pytest.mark.asyncio
async def test_anima_lora_service_reports_anima_model_type():
    """The Anima service reuses LoRA logic under the distinct model type."""

    from py.services.anima_lora_scanner import AnimaLoraScanner
    from py.services.anima_lora_service import AnimaLoraService

    scanner = await AnimaLoraScanner.get_instance()
    service = AnimaLoraService(scanner)

    assert service.model_type == "anima_loras"
    assert service.scanner is scanner
