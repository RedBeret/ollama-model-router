# Contributing

## Development setup

```bash
git clone https://github.com/RedBeret/ollama-model-router.git
cd ollama-model-router
pip install -e ".[dev]"
```

## Running tests

```bash
pytest -v
```

CI runs tests on Ubuntu, macOS, and Windows against Python 3.10, 3.11, 3.12, and 3.13.

## Pull request guidelines

- Branch from `main`, one feature or fix per PR
- Add tests for new routing logic or config behavior
- Tests must pass on all three platforms before requesting review
- No direct pushes to `main`
- Model assignments in `config.example.yaml` reflect current free-tier availability — update with benchmarks when changing defaults

## Adding a new model category

1. Add the category name to `model_router/categorizer.py` under the keyword lists
2. Add a default model assignment to `config.example.yaml`
3. Add a test case to `tests/test_categorizer.py`
4. Update the default model assignments table in `README.md`

All example prompts in tests and documentation are synthetic.
