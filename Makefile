# CML MCP Server

.DEFAULT_GOAL := help

IMAGE_NAME := cml-mcp-server

.PHONY: build
build: ## Build Docker image - requires CLOUDERA_ML_HOST env var
	@if [ -z "$$CLOUDERA_ML_HOST" ]; then \
		echo "Error: CLOUDERA_ML_HOST environment variable required"; \
		echo "Usage: CLOUDERA_ML_HOST=https://your-cml-instance.cloudera.site make build"; \
		exit 1; \
	fi
	docker build --build-arg CLOUDERA_ML_HOST=$$CLOUDERA_ML_HOST -t $(IMAGE_NAME) .
.PHONY: run
run: ## Run in STDIO mode (for Claude Desktop)
	docker run -i --rm $(IMAGE_NAME)

.PHONY: run-secrets
run-secrets: ## Run with Docker secrets
	docker-compose -f docker-compose.secrets.yml run --rm cml-mcp-server

.PHONY: test
test: ## Test STDIO transport
	.venv/bin/python tests/test_cml_mcp_client.py --quick

.PHONY: clean
clean: ## Remove Docker image
	docker rmi $(IMAGE_NAME) || true

.PHONY: dev
dev: ## Install for local development
	uv sync

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'