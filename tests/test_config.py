"""Tests for config loading."""

import os
import tempfile
import yaml

from model_router.config import load_config


def test_default_config():
    config = load_config("/nonexistent/path.yaml")
    assert config["ollama_url"] == "http://localhost:11434"
    assert config["default_category"] == "chat"


def test_custom_config():
    custom = {"ollama_url": "http://myserver:11434", "default_category": "code"}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(custom, f)
        path = f.name

    try:
        config = load_config(path)
        assert config["ollama_url"] == "http://myserver:11434"
        assert config["default_category"] == "code"
    finally:
        os.unlink(path)
