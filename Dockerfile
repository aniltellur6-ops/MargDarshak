FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ /app/backend/
COPY scripts/ /app/scripts/

# Set Python path so imports from backend work correctly
ENV PYTHONPATH=/app

# Expose the API port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
