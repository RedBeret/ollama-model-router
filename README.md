# ollama-model-router

Auto-picks the best free Ollama cloud model for your prompt. Stop guessing which model to use - just ask and it routes to the right one.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/RedBeret/ollama-model-router/actions/workflows/ci.yml/badge.svg)](https://github.com/RedBeret/ollama-model-router/actions/workflows/ci.yml)

## How it works

```
Your prompt --> Categorizer (detects task type)
                    |
              code / reasoning / chat / vision / search
                    |
              Model Registry (picks best model for category)
                    |
              Health Check (is the model responding?)
                    |
              Send request with retry/fallback
                    |
              Stream response back to you
```

## Install

Works on macOS, Linux and Windows.

```bash
# from source
git clone https://github.com/RedBeret/ollama-model-router.git
cd ollama-model-router
pip install -e .
```

## Quick start

```bash
model-router "write a python function to parse CSV files"
# -> routes to minimax-m2.7:cloud (best for code)

# or run as module
python -m model_router "write a python function to parse CSV files"
```

## Features

- Auto-detects prompt type (code, reasoning, chat, vision, search)
- Routes to the best free cloud model for that task
- Falls back to alternate models if primary is down
- Configurable model preferences via YAML
- Rate limit handling with automatic retry
- Interactive chat mode with model switching

## Default model assignments

| Category | Model | Why |
|----------|-------|-----|
| chat | kimi-k2.5:cloud | best all-around quality |
| code | minimax-m2.7:cloud | top coding benchmarks |
| reasoning | gpt-oss:120b-cloud | fast reasoning |
| vision | gemma4:cloud | multimodal support |
| fast | nemotron-3-nano:cloud | when speed matters most |

## Usage

```bash
# auto-route based on prompt
python -m model_router "explain quicksort step by step"

# force a specific category
python -m model_router --category code "refactor this function"

# force a specific model
python -m model_router --model kimi-k2.5:cloud "hello"

# interactive chat
python -m model_router --interactive

# list available models
python -m model_router --list
```

## Configuration

Copy `config.example.yaml` to `config.yaml` and customize:

```yaml
ollama_url: http://localhost:11434
default_category: chat
models:
  chat:
    primary: kimi-k2.5:cloud
    fallback: glm-5:cloud
  code:
    primary: minimax-m2.7:cloud
    fallback: devstral-2:cloud
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running (`ollama serve`)
- Internet connection (for cloud models)

## See also

- [awesome-ollama-models](https://github.com/RedBeret/awesome-ollama-models) - curated list of all Ollama cloud models with benchmarks and use case recommendations

## License

[MIT](LICENSE)
