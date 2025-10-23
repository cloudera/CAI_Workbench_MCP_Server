# CAI Workbench MCP Server

.DEFAULT_GOAL := help

IMAGE_NAME := cai-workbench-mcp-server

.PHONY: build
build: ## Build Docker image - requires CAI_WORKBENCH_HOST env var
	@if [ -z "$$CAI_WORKBENCH_HOST" ]; then \
		echo "Error: CAI_WORKBENCH_HOST environment variable required"; \
		echo "Usage: CAI_WORKBENCH_HOST=https://your-cai-instance.cloudera.site make build"; \
		exit 1; \
	fi
	docker build --build-arg CAI_WORKBENCH_HOST=$$CAI_WORKBENCH_HOST -t $(IMAGE_NAME) .
.PHONY: run
run: ## Run in STDIO mode (for Claude Desktop)
	docker run -i --rm $(IMAGE_NAME)

.PHONY: run-secrets
run-secrets: ## Run with Docker secrets
	docker-compose -f docker-compose.secrets.yml run --rm cai-workbench-mcp-server

.PHONY: test
test: ## Test STDIO transport
	.venv/bin/python tests/test_cai_mcp_client.py --quick

.PHONY: clean
clean: ## Remove Docker image
	docker rmi $(IMAGE_NAME) || true

.PHONY: dev
dev: ## Install for local development
	uv sync

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'