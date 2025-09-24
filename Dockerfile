# Simple, fast Dockerfile using UV
FROM python:3.12-slim

# Build argument for Cloudera ML host URL
ARG CLOUDERA_ML_HOST

# Install system dependencies and UV
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && mv /root/.local/bin/uvx /usr/local/bin/uvx

# Create non-root user
RUN groupadd -r cml && useradd -r -g cml cml

# Set working directory
WORKDIR /app

# Copy project files
COPY --chown=cml:cml pyproject.toml uv.lock ./
COPY --chown=cml:cml cml_mcp_server/ ./cml_mcp_server/

# Install dependencies with UV (much faster than pip!)
RUN uv sync --frozen

# Install Cloudera ML API (required dependency not in pyproject.toml)
# Extract domain from CLOUDERA_ML_HOST (strip https://)
RUN if [ -n "${CLOUDERA_ML_HOST}" ]; then \
        CML_DOMAIN=$(echo "${CLOUDERA_ML_HOST}" | sed 's|https\?://||' | sed 's|/$||'); \
        uv pip install https://${CML_DOMAIN}/api/v2/python.tar.gz; \
    else \
        echo "Error: CLOUDERA_ML_HOST build argument required"; \
        exit 1; \
    fi

# Switch to non-root user
USER cml

# Activate UV environment
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Expose port for HTTP mode
EXPOSE 8080

# Default to stdio mode (like Terraform MCP server)
CMD ["python", "-m", "cml_mcp_server.stdio_server"]