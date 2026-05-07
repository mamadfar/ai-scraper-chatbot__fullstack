
# ─── Variables ───────────────────────────────────────────────────────────────
PYTHON     := uv run
APP        := app.main:app
TEST_DIR   := tests
COV_TARGET := app

.PHONY: install dev test test-cov lint format type-check \
		clean scrape ingest docker-build docker-up docker-down help

#? ─── Default target (runs when we just type `make`) ─────────────────────────
DEFAULT_GOAL := help

#? ─── Setup ───────────────────────────────────────────────────────────────────
install:	## Install all dependencies
	uv sync

install-browsers: 	## Install Playwright browsers (needed for scraping)
	$(PYTHON) playwright install chromium

#? ─── Development ─────────────────────────────────────────────────────────────
dev:	## Start FastAPI dev server with hot reload
	$(PYTHON) uvicorn $(APP) --reload --port 8000

#? ─── Testing ─────────────────────────────────────────────────────────────────
test:	## Run all tests
	$(PYTHON) pytest $(TEST_DIR) -v		## -v for verbose output

test-cov:	## Run tests with coverage report
	$(PYTHON) pytest $(TEST_DIR) -v \
		--cov=$(COV_TARGET) \
		--cov-report=term-missing \ 	## Show missing coverage in terminal
		--cov-report=html		## Generate HTML coverage report

test-watch: 	## Run tests in watch mode
	$(PYTHON) pytest-watch $(TEST_DIR)

#? ─── Code Quality ────────────────────────────────────────────────────────────
lint: 	## Run ruff linter
	$(PYTHON) ruff check $(APP)

format: 	## Auto-format code with ruff
	$(PYTHON) ruff format $(APP)

type-check: 	## Run mypy type checker
	$(PYTHON) mypy $(APP)

check: lint type-check 	## Run all checks (lint + types)

#? ─── AI Pipeline ─────────────────────────────────────────────────────────────
scrape: 	## Run the web scraper
	$(PYTHON) python -m app.modules.scraper.run

ingest: 	## Run full ingestion pipeline (scrape + embed + store)
	$(PYTHON) python -m app.modules.ingestion.run

#? ─── Docker ──────────────────────────────────────────────────────────────────
docker-build: 	## Build Docker images
	docker compose build

docker-up: 	## Start all services
	docker compose up -d 	# -d for detached mode (background)

