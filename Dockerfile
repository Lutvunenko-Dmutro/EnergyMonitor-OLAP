# ═══════════════════════════════════════════════════════════════
# Production Dockerfile for Energy Monitor Ultimate
# ═══════════════════════════════════════════════════════════════
#
# Build: docker build -t energy-monitor:latest .
# Run:   docker run -p 8501:8501 energy-monitor:latest
# Env:   docker run -p 8501:8501 --env-file .env energy-monitor:latest

FROM python:3.11-slim

# ───────────────────────────────────────────────────────────────
# METADATA & LABELS
# ───────────────────────────────────────────────────────────────
LABEL maintainer="Energy Monitor Team"
LABEL description="Energy Monitor Ultimate - OLAP & AI Forecasting System"
LABEL version="2.4.0"

# ───────────────────────────────────────────────────────────────
# ENVIRONMENT SETUP
# ───────────────────────────────────────────────────────────────
WORKDIR /app

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Disable pip cache
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Streamlit configuration
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_LOGGER_LEVEL=info
ENV STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false

# ───────────────────────────────────────────────────────────────
# SYSTEM DEPENDENCIES
# ───────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ───────────────────────────────────────────────────────────────
# PYTHON DEPENDENCIES
# ───────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# ───────────────────────────────────────────────────────────────
# APPLICATION CODE
# ───────────────────────────────────────────────────────────────
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 streamlit && \
    chown -R streamlit:streamlit /app

USER streamlit

# ───────────────────────────────────────────────────────────────
# HEALTH CHECK
# ───────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ───────────────────────────────────────────────────────────────
# EXPOSE & ENTRYPOINT
# ───────────────────────────────────────────────────────────────
EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]
