# ---------- Script 1 ----------
FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8123"]
# ---------- Script 1 ----------

# ---------- Script 1 with VENV ----------
# FROM python:3.10-slim
#
# # Create a virtual environment
# RUN python -m venv /venv
# # Set the virtual environment path
# ENV PATH="/venv/bin:$PATH"
#
# WORKDIR /app
# COPY requirements.txt .
# # Install dependencies in the virtual environment
# RUN pip install --no-cache-dir -r requirements.txt
#
# COPY ./app ./app
#
# # Activate virtual environment and run the application
# CMD ["/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8123"]
# ---------- Script 1 with VENV ----------

# ---------- Script 2 ----------
# Stage 1: Build Environment
# FROM python:3.10 as builder
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --user -r requirements.txt
#
# # Stage 2: Runtime Environment
# FROM python:3.10-slim
# WORKDIR /app
# COPY --from=builder /root/.local /root/.local
# COPY . .
#
# # Ensure scripts in .local are usable
# ENV PATH=/root/.local/bin:$PATH
#
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8123"]
# ---------- Script 2 ----------

# ---------- Script 3 ----------
# # Stage 1: Build Environment
# FROM python:3.10-slim as builder
#
# RUN python -m venv /vgarbage
# ENV PATH="/vgarbage/bin:$PATH"
#
# WORKDIR /app
# COPY requirements.txt .
#
# RUN pip install --no-cache-dir -r requirements.txt
#
# # Stage 2: Runtime Environment
# FROM python:3.10-slim
# COPY --from=builder /vgarbage /vgarbage
# ENV PATH="/vgarbage/bin:$PATH"
#
# WORKDIR /app
# COPY . .
#
# RUN rm -rf /root/.cache/pip
#
# CMD [ "uvcorn", "main.app", "--host", "0.0.0.0", "--port", "8123" ]
# ---------- Script 3 ----------

# ---------- Script 7 (Most Optimized) ----------
# # Multi-stage build with dependency optimization
# FROM python:3.10-slim as builder
#
# # Install build dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends gcc && \
#     rm -rf /var/lib/apt/lists/*
#
# # Set up working directory
# WORKDIR /app
#
# # Copy requirements and install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
#
# # Production stage - minimal image
# FROM python:3.10-slim
#
# # Set environment variables for performance
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     PYTHONPATH=/app
#
# # Create non-root user
# RUN groupadd -r appgroup && \
#     useradd -r -g appgroup appuser
#
# # Copy only the necessary Python dependencies
# COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
#
# # Set up working directory
# WORKDIR /app
#
# # Copy only the application code
# COPY ./app ./app
#
# # Change ownership to non-root user
# RUN chown -R appuser:appgroup /app
#
# # Switch to non-root user
# USER appuser
#
# # Expose port
# EXPOSE 8123
#
# # Run application
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8123"]
# ---------- Script 7 (Most Optimized) ----------
