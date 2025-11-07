# Build stage
FROM python:3.12-slim AS builder

# Install uv for fast dependency management
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
COPY csiro/ ./csiro/
RUN uv sync --frozen --no-dev
RUN uv pip install --python /app/.venv/bin/python --no-deps -e .

# Runtime stage
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/csiro /app/csiro
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

# Create data directory
RUN mkdir -p /app/data

# Set environment variables - add .venv/bin to PATH so 'csiro' command is found
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

ENTRYPOINT ["csiro"]
