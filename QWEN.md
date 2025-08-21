# Garbage Classifier API - Qwen Context

## Project Overview

This is a FastAPI-based API for garbage classification using the CLIP (Contrastive Language-Image Pretraining) model. It performs zero-shot image classification, meaning it can classify images into categories it wasn't specifically trained on.

### Main Technologies
- **FastAPI**: Modern, fast web framework for building APIs with Python 3.7+
- **CLIP Model**: OpenAI's Contrastive Language-Image Pre-training model from Hugging Face
- **PyTorch**: Deep learning framework
- **Transformers**: Hugging Face library for state-of-the-art NLP and vision models
- **Pillow**: Python Imaging Library for image processing
- **Uvicorn**: ASGI server for running the FastAPI application

### Architecture
The application follows a simple architecture:
1. FastAPI handles HTTP requests and responses
2. Images are processed using Pillow
3. CLIP model performs zero-shot classification
4. Results are returned as JSON with confidence scores

## Building and Running

### Prerequisites
- Python 3.7+
- pip package manager

### Installation
```bash
# Create a virtual environment
python -m venv v_garbage_classifier

# Activate the virtual environment
source v_garbage_classifier/bin/activate  # On Linux/Mac
# or
v_garbage_classifier\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8123

# Or using Python
python -m uvicorn app.main:app --host 0.0.0.0 --port 8123
```

### Running with Docker
```bash
# Build the Docker image
docker build -t garbage-classifier .

# Run the container
docker run -p 8123:8123 garbage-classifier
```

### Accessing the API
- API Documentation: http://localhost:8123/api/docs
- Base URL: http://localhost:8123

## API Endpoints

### GET /
- Returns a welcome message
- Used to verify the API is running

### POST /classify
- Accepts an image file and optional comma-separated categories
- Returns classification results with confidence scores

#### Parameters:
- `file` (required): Image file of garbage item
- `categories` (optional): Comma-separated list of categories to classify against

#### Default Categories:
- plastic bottle
- glass bottle
- paper
- cardboard
- metal can
- organic waste
- electronic waste
- textile

#### Example Request:
```bash
curl -X POST "http://localhost:8123/classify" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@image.jpg"
```

#### Example Response:
```json
{
  "top_class": "electronic waste",
  "confidence": 0.33171185851097107,
  "predictions": {
    "plastic bottle": 0.24136486649513245,
    "glass bottle": 0.0022902777418494225,
    "paper": 0.0015287415590137243,
    "cardboard": 0.0012100355233997107,
    "metal can": 0.24120794236660004,
    "organic waste": 0.18023031949996948,
    "electronic waste": 0.33171185851097107,
    "textile": 0.00045594872790388763
  }
}
```

## Development Conventions

### Code Structure
- `app/main.py`: Main FastAPI application and endpoints
- `app/clip_model.py`: CLIP model loading and classification logic
- `app/utils.py`: Utility functions for image processing
- `app/test.py`: Simple test endpoint
- `requirements.txt`: Python dependencies
- `dockerfile`: Docker configuration for containerization

### Adding New Categories
To modify the default categories, update the `DEFAULT_CLASSES` array in `app/main.py`.

### Model Information
The application uses the `openai/clip-vit-base-patch32` model from Hugging Face, which is loaded once at startup for efficiency.

### Error Handling
The API includes basic error handling that logs exceptions and returns error messages in JSON format.

## Testing
Simple testing can be done using curl commands or the interactive API documentation at `/api/docs`.