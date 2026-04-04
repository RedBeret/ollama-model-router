"""Load config from yaml file."""

import os
import yaml


DEFAULT_CONFIG = {
    "ollama_url": "http://localhost:11434",
    "default_category": "chat",
    "rate_limit": {
        "max_requests_per_minute": 15,
        "retry_after_seconds": 30,
        "max_retries": 3,
    },
}


def load_config(path=None) -> dict:
    """Load config from yaml file. Falls back to defaults if not found."""
    if path is None:
        path = os.path.join(os.getcwd(), "config.yaml")

    config = dict(DEFAULT_CONFIG)

    if os.path.exists(path):
        with open(path) as f:
            user_config = yaml.safe_load(f) or {}
        config.update(user_config)

    return config
