
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

docker-down: 	## Stop all services
	docker compose down

docker-logs: 	## Tail logs from all services
	docker compose logs -f 		## -f for follow mode (tail)

docker-clean: 	## Stop services and remove volumes (⚠️ deletes DB data)

#? ─── Cleanup ─────────────────────────────────────────────────────────────────
clean: 	## Remove all Docker artifacts (including volumes, cache, build, etc)
	find . -type d -name __pycache__ -exec rm -rf {} +		## d means directory, -name means search for a specific name
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf htmlcov .coverage coverage.xml

#? ─── Help ────────────────────────────────────────────────────────────────────
help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'