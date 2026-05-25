# =============================================================================
# Pi-Scope developer task runner.
# Run `make help` to list the available targets.
# =============================================================================
.DEFAULT_GOAL := help
.PHONY: help install install-backend install-frontend dev-backend dev-frontend \
        test lint format build docker-up docker-down clean

BACKEND := backend
FRONTEND := frontend

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: install-backend install-frontend ## Install all dependencies.

install-backend: ## Install backend (Python) dependencies.
	cd $(BACKEND) && pip install -r requirements-dev.txt

install-frontend: ## Install frontend (Node) dependencies.
	cd $(FRONTEND) && npm install

dev-backend: ## Run the FastAPI dev server with autoreload.
	cd $(BACKEND) && PISCOPE_DEBUG=true uvicorn app.main:app --reload --port 8000

dev-frontend: ## Run the Vite dev server.
	cd $(FRONTEND) && npm run dev

test: ## Run the backend test suite.
	cd $(BACKEND) && pytest

lint: ## Lint backend (ruff) and frontend (eslint + tsc).
	cd $(BACKEND) && ruff check . && mypy app
	cd $(FRONTEND) && npm run lint && npm run typecheck

format: ## Auto-format the backend with ruff.
	cd $(BACKEND) && ruff format . && ruff check --fix .

build: ## Build the production frontend bundle.
	cd $(FRONTEND) && npm run build

docker-up: ## Build and start the full stack with Docker Compose.
	docker compose up --build

docker-down: ## Stop and remove the Docker Compose stack.
	docker compose down

clean: ## Remove caches and build artefacts.
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf $(BACKEND)/.pytest_cache $(BACKEND)/.ruff_cache $(BACKEND)/.mypy_cache
	rm -rf $(FRONTEND)/dist
