# This dockerfile looks this way to optimize on storage space. Probably not super necessary.
# Build stage
FROM python:3.12-slim-bookworm AS builder
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remove compiled python files and build artifacts
RUN find /opt/venv -name "*.pyc" -delete && \
    find /opt/venv -name "__pycache__" -delete

FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && \
    # Add 'contrib' to the package sources
    sed -i 's/main$/main contrib/g' /etc/apt/sources.list 2>/dev/null || \
    sed -i '/^Components:/ s/$/ contrib/' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    # Pre-accept the Microsoft EULA
    echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections && \
    # Install the installer and font-management tools
    apt-get install -y --no-install-recommends \
        ttf-mscorefonts-installer \
        fontconfig && \
    # Refresh the font cache
    fc-cache -f -v && \
    # Clean up to save space
    apt-get purge -y --auto-remove && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
COPY . .

ENV PATH="/opt/venv/bin:$PATH"
# Prevents Python from writing .pyc files to the container disk
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8501
ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true" ]