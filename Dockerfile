# ===== BUILDER STAGE =====
FROM python:3.11.13-slim-bookworm AS builder

ENV ENV=production

# Install build deps (only for packages needing compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:0.7.20 /uv /uvx /bin/

WORKDIR /pkg

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies into container’s Python env
RUN uv sync --frozen --no-cache --python=/usr/local/bin/python3.11

# ===== RUNTIME STAGE =====
FROM python:3.11.13-slim-bookworm AS runtime

# Runtime deps only (drop build-essential etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:0.7.20 /uv /uvx /bin/

WORKDIR /pkg

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy your app
COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "main.py"]