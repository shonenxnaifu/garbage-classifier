import logging

from fastapi import FastAPI, File, Query, UploadFile

from app.clip_model import classify_image
from app.utils import load_image

app = FastAPI(
    title="Garbage Zero-Shot Classifier",
    description="Classify garbage types using CLIP without training",
    version="1.0",
)

# Default garbage categories (customizable via API)
DEFAULT_CLASSES = [
    "plastic bottle",
    "glass bottle",
    "paper",
    "cardboard",
    "metal can",
    "organic waste",
    "electronic waste",
    "textile",
]


@app.post("/classify")
async def classify(
    file: UploadFile = File(..., description="Image of garbage item"),
    categories: str = Query(
        default=",".join(DEFAULT_CLASSES),
        description="Comma-separated classification categories",
    ),
):
    try:
        # Process inputs
        candidate_labels = [c.strip() for c in categories.split(",")]

        # Add debug logging
        print(f"Received file: {file.filename}")
        print(f"Content type: {file.content_type}")

        image = load_image(await file.read())

        # Run classification
        results = classify_image(image, candidate_labels)

        # Find top prediction
        top_class = max(results, key=results.get)

        return {
            "top_class": top_class,
            "confidence": results[top_class],
            "predictions": results,
        }

    except Exception as e:
        logging.error(f"Classification error: {str(e)}")
        return {"error": "Classification failed"}
