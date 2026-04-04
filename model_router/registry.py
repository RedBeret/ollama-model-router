"""Model registry - maps categories to preferred models."""

DEFAULT_MODELS = {
    "chat": {
        "primary": "kimi-k2.5:cloud",
        "fallback": "glm-5:cloud",
    },
    "code": {
        "primary": "minimax-m2.7:cloud",
        "fallback": "devstral-2:cloud",
    },
    "reasoning": {
        "primary": "gpt-oss:120b-cloud",
        "fallback": "deepseek-v3.2:cloud",
    },
    "vision": {
        "primary": "gemma4:cloud",
        "fallback": "qwen3-vl:cloud",
    },
    "search": {
        "primary": "kimi-k2.5:cloud",
        "fallback": "qwen3.5:cloud",
    },
    "fast": {
        "primary": "nemotron-3-nano:cloud",
        "fallback": "ministral-3:cloud",
    },
}


class ModelRegistry:
    def __init__(self, custom_models=None):
        self.models = dict(DEFAULT_MODELS)
        if custom_models:
            for cat, config in custom_models.items():
                self.models[cat] = config

    def get_primary(self, category: str) -> str:
        entry = self.models.get(category, self.models["chat"])
        return entry["primary"]

    def get_fallback(self, category: str) -> str:
        entry = self.models.get(category, self.models["chat"])
        return entry.get("fallback", entry["primary"])

    def list_categories(self) -> list:
        return list(self.models.keys())

    def list_models(self) -> dict:
        result = {}
        for cat, config in self.models.items():
            result[cat] = {
                "primary": config["primary"],
                "fallback": config.get("fallback", config["primary"]),
            }
        return result
