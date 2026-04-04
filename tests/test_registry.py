"""Tests for model registry."""

from model_router.registry import ModelRegistry


def test_default_models():
    registry = ModelRegistry()
    assert registry.get_primary("chat") == "kimi-k2.5:cloud"
    assert registry.get_primary("code") == "minimax-m2.7:cloud"
    assert registry.get_primary("reasoning") == "gpt-oss:120b-cloud"


def test_fallback():
    registry = ModelRegistry()
    assert registry.get_fallback("code") == "devstral-2:cloud"


def test_custom_models():
    custom = {"code": {"primary": "custom-model:cloud", "fallback": "other:cloud"}}
    registry = ModelRegistry(custom_models=custom)
    assert registry.get_primary("code") == "custom-model:cloud"
    assert registry.get_primary("chat") == "kimi-k2.5:cloud"


def test_unknown_category_falls_back_to_chat():
    registry = ModelRegistry()
    assert registry.get_primary("nonexistent") == "kimi-k2.5:cloud"


def test_list_categories():
    registry = ModelRegistry()
    cats = registry.list_categories()
    assert "chat" in cats
    assert "code" in cats
    assert "reasoning" in cats


def test_list_models():
    registry = ModelRegistry()
    models = registry.list_models()
    assert "chat" in models
    assert "primary" in models["chat"]
    assert "fallback" in models["chat"]
