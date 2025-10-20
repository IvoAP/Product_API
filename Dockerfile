FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 
ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONPATH="/app"

# Set work directory
WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock

# Install dependencies using uv with system flag
RUN uv pip install --system fastapi uvicorn python-dotenv sqlalchemy pytest

# Copy application code
COPY app/ /app/app/

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]