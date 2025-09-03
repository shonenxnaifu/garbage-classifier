# Docker Build Diagnosis and Solutions

## Issue Summary
When trying to build a Docker image using Alpine Linux as the base image, the build fails due to compatibility issues between PyTorch and Alpine's musl libc.

## Error Details
The specific error was:
```
OSError: Error relocating /usr/local/lib/python3.10/site-packages/torch/lib/libgomp-a34b3233.so.1: pthread_attr_setaffinity_np: symbol not found
```

This error occurs because PyTorch's compiled libraries expect glibc symbols that are not available in Alpine's musl libc implementation.

## Root Cause
Alpine Linux uses musl libc instead of glibc. PyTorch and many other scientific Python packages have compiled C/C++ extensions that are built against glibc and are not compatible with musl libc.

## Solutions

### 1. Recommended Solution: Use Debian-based Slim Image (Working)
The `python:3.10-slim` base image uses Debian and glibc, making it fully compatible with PyTorch.

**Dockerfile.slim-final:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Create a non-privileged user
RUN useradd --create-home appuser
WORKDIR /app
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8123

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8123"]
```

### 2. Alternative Solution: Fixed Alpine with Build Dependencies (Builds but has runtime issues)
While we can install the necessary build dependencies to get the image to build, PyTorch still has runtime compatibility issues with Alpine.

**Dockerfile.alpine-final:**
```dockerfile
FROM python:3.10-alpine

# Install build dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies to reduce image size
RUN apk del gcc musl-dev linux-headers

COPY ./app ./app

# Create a non-privileged user
RUN adduser -D appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8123

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8123"]
```

### 3. Experimental Solution: Multi-stage Alpine (Not recommended for PyTorch apps)
This approach attempts to reduce image size but still has the same compatibility issues.

## Image Size Comparison
| Image Type | Size |
|------------|------|
| Slim (Recommended) | 1.13GB |
| Alpine (Fixed) | 1.26GB |
| Alpine (Optimized) | 1.09GB |

## Recommendation
Use the Debian-based slim image (`python:3.10-slim`) for applications that use PyTorch or other scientific Python packages with compiled extensions. While Alpine images are generally smaller, the compatibility issues with PyTorch make it unsuitable for this particular application.

If image size is a critical concern, consider:
1. Using a multi-stage build with the slim image
2. Removing unnecessary dependencies from requirements.txt
3. Using PyTorch's CPU-only version (already implemented)
4. Exploring alternative models that are more compatible with Alpine

## Running the Container
```bash
docker run -d -p 8111:8123 --name=classifier-api waste-classifier-slim-final
```

The API will be available at http://localhost:8111/api/docs