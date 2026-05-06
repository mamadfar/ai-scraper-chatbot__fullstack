
# Structure
```md
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  ← FastAPI app entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            ← already done in Step 2
│   │   └── exceptions.py        ← global error classes
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── error_handler.py     ← global error handler
│   └── modules/
│       └── health/
│           ├── __init__.py
│           ├── router.py        ← route definitions
│           └── schemas.py       ← Pydantic models for this module
├── tests/
│   ├── __init__.py
│   └── test_health.py
```

## IDE / import completion

If imports (stdlib or deps) do not autocomplete in Cursor/VS Code:

- **Interpreter:** use **Python: Select Interpreter** and pick `.venv\Scripts\python.exe` under this folder so Pylance sees installed packages.
- **Monorepo:** if the workspace root is the parent repo (`ai-chatbot`), the wrong interpreter is the usual cause; optional: set `python.defaultInterpreterPath` in `.vscode/settings.json` to this `.venv`.
- **Extensions:** ensure the Python extension is on and the language server is Pylance (not “None”); reload after changing the interpreter.
- **Missing packages:** run `uv sync` here so the venv matches `pyproject.toml`.

## UV

| UV | pnpm equivalent | What it does |
| --- | --- | --- |
| `uv init` | `pnpm init` | Create new project |
| `uv add fastapi` | `pnpm add fastapi` | Add dependency |
| `uv add --dev pytest` | `pnpm add -D pytest` | Add dev dependency |
| `uv remove fastapi` | `pnpm remove fastapi` | Remove dependency |
| `uv sync` | `pnpm install` | Install all deps from lockfile |
| `uv run pytest` | `pnpm test` | Run a command in the venv |
| `uv run python main.py` | `node dist/main.js` | Run a Python file |
| `uv lock` | `pnpm install --frozen-lockfile` | Regenerate lockfile |
| `uv python install 3.12` | `nvm install 20` | Install Python version |
