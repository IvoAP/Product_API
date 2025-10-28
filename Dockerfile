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
# (Optional) Copy lock file if you generate one later; harmless if missing
COPY uv.lock /app/uv.lock

# Install project dependencies directly from pyproject.toml
RUN uv pip install --system .

# Copy application code
COPY app/ /app/app/
COPY alembic.ini /app/alembic.ini
COPY migrations/ /app/migrations/
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Command to run the startup script (migrate, seed, serve)
CMD ["./start.sh"]