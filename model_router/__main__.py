"""CLI entry point for model router."""

import argparse
import sys

from .categorizer import categorize
from .registry import ModelRegistry
from .client import OllamaClient


def main():
    parser = argparse.ArgumentParser(
        description="Auto-route prompts to the best Ollama cloud model"
    )
    parser.add_argument("prompt", nargs="?", help="prompt to send")
    parser.add_argument("--model", "-m", help="force a specific model")
    parser.add_argument("--category", "-c", help="force a category (chat, code, reasoning, vision, search, fast)")
    parser.add_argument("--list", "-l", action="store_true", help="list model assignments")
    parser.add_argument("--no-stream", action="store_true", help="disable streaming output")
    parser.add_argument("--url", default="http://localhost:11434", help="ollama server url")

    args = parser.parse_args()

    registry = ModelRegistry()
    client = OllamaClient(args.url)

    if args.list:
        models = registry.list_models()
        for cat, config in models.items():
            print(f"  {cat:12s}  {config['primary']:30s}  (fallback: {config['fallback']})")
        return

    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    if args.model:
        model = args.model
        category = "manual"
    else:
        category = args.category or categorize(args.prompt)
        model = registry.get_primary(category)

        if not client.health_check(model):
            fallback = registry.get_fallback(category)
            print(f"[router] {model} unavailable, falling back to {fallback}", file=sys.stderr)
            model = fallback

    print(f"[router] category={category} model={model}", file=sys.stderr)

    if args.no_stream:
        response = client.generate(model, args.prompt, stream=False)
        print(response)
    else:
        for chunk in client.generate(model, args.prompt, stream=True):
            print(chunk, end="", flush=True)
        print()


if __name__ == "__main__":
    main()
