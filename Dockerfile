# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NODE_ENV=production

# Install system dependencies (including Node.js for Reflex)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY database.py .
COPY ai_service.py .
COPY rxconfig.py .
COPY app_reflex/ ./app_reflex/
COPY assets/ ./assets/

# Initialize Reflex (this will install node dependencies)
RUN reflex init

# Create directory for SQLite database
RUN mkdir -p /app/data

# Expose ports for both backend and frontend
EXPOSE 8000 3000

# Create startup script to run both backend and frontend
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Start FastAPI backend in background\n\
uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
BACKEND_PID=$!\n\
\n\
# Start Reflex frontend\n\
reflex run --env prod --backend-only &\n\
REFLEX_PID=$!\n\
\n\
# Function to handle shutdown\n\
shutdown() {\n\
    echo "Shutting down services..."\n\
    kill $BACKEND_PID $REFLEX_PID 2>/dev/null || true\n\
    wait $BACKEND_PID $REFLEX_PID 2>/dev/null || true\n\
    exit 0\n\
}\n\
\n\
# Trap signals\n\
trap shutdown SIGTERM SIGINT\n\
\n\
# Wait for both processes\n\
wait -n\n\
EXIT_CODE=$?\n\
shutdown\n\
exit $EXIT_CODE\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"]
