"""Ollama API client with health checks and streaming."""

import json
import requests


class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def health_check(self, model: str, timeout: int = 5) -> bool:
        """Check if a model is available and responding."""
        try:
            resp = self.session.post(
                f"{self.base_url}/api/generate",
                json={"model": model, "prompt": "hi", "stream": False},
                timeout=timeout,
            )
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def generate(self, model: str, prompt: str, stream: bool = True, timeout: int = 60):
        """Send a prompt to a model. Returns response text or yields chunks if streaming."""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
        }

        if stream:
            return self._stream_response(payload, timeout)
        else:
            return self._blocking_response(payload, timeout)

    def _stream_response(self, payload: dict, timeout: int):
        """Yield response chunks as they arrive."""
        resp = self.session.post(
            f"{self.base_url}/api/generate",
            json=payload,
            stream=True,
            timeout=timeout,
        )
        resp.raise_for_status()

        for line in resp.iter_lines():
            if not line:
                continue
            data = json.loads(line)
            if "response" in data:
                yield data["response"]
            if data.get("done"):
                break

    def _blocking_response(self, payload: dict, timeout: int) -> str:
        """Wait for full response and return it."""
        resp = self.session.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=timeout,
        )
        resp.raise_for_status()
        return resp.json().get("response", "")

    def list_models(self) -> list:
        """List locally available models."""
        try:
            resp = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            resp.raise_for_status()
            return [m["name"] for m in resp.json().get("models", [])]
        except requests.RequestException:
            return []
