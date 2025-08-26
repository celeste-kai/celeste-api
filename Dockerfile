# syntax=docker/dockerfile:1.7-labs
# Builder stage
FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# System deps for build
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies into a venv at /app/.venv (cached)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --frozen

# Copy source and install project into venv
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen

# Runtime stage
FROM python:3.13-slim AS runtime

# Copy uv for potential runtime usage (optional)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /app

# Copy virtualenv and app code from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/v1/health')" || exit 1

CMD ["uvicorn", "celeste_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
