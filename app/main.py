import logging
from typing import Dict

from fastapi import FastAPI, File, Query, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.clip_model import classify_image
from app.utils import load_image

app = FastAPI(
    title="Garbage Zero-Shot Classifier",
    description="Classify garbage types using CLIP with pretrained model",
    version="1.0",
    contact={"name": "Pawitra Warda", "email": "pawitrawarda@gmail.com"},
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json",
    openapi_tags=[
        {
            "name": "Waste Classification",
            "description": "Endpoints for garbage identification",
        }
    ],
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

# Extended categories from WASTE_DEFINITION.md
EXTENDED_CLASSES = [
    "food scraps", "vegetable waste", "fruit peels", "coffee grounds", "tea leaves", 
    "egg shells", "yard trimmings", "grass clippings", "fallen leaves", "plant debris", 
    "wood chips", "paper towels", "food-soiled paper", "compostable materials", 
    "biodegradable waste", "organic matter", "chemical containers", "paint cans", 
    "solvent bottles", "batteries", "lead-acid batteries", "lithium batteries", 
    "medical waste", "used syringes", "medical sharps", "infectious waste", 
    "pharmaceuticals", "expired medicines", "pesticide containers", "herbicide bottles", 
    "toxic substances", "flammable materials", "corrosive liquids", "electronic waste", 
    "e-waste", "packaging materials", "plastic packaging", "food containers", 
    "disposable utensils", "discarded clothing", "worn-out textiles", "household goods", 
    "broken furniture", "discarded appliances", "non-recyclable plastics", "mixed waste", 
    "general trash", "landfill waste", "bulky waste", "construction debris", 
    "demolition waste", "wastewater", "used cooking oil", "motor oil", 
    "industrial discharge", "chemical wastewater", "medical liquids", "contaminated water", 
    "sewage water", "liquid chemicals", "solvent waste", "paint waste", "cleaning solutions", 
    "detergent wastewater", "laboratory liquids", "photographic chemicals", "plastic bottles", 
    "PET containers", "HDPE containers", "paper products", "cardboard boxes", 
    "office paper", "newspapers", "magazines", "glass bottles", "glass jars", 
    "aluminum cans", "tin cans", "metal containers", "scrap metal", "electronics recycling", 
    "recyclable packaging", "clear plastic", "colored glass"
]

# Remove duplicates while preserving order
UNIQUE_EXTENDED_CLASSES = list(dict.fromkeys(EXTENDED_CLASSES))

# Ensure DEFAULT_CLASSES items are also included
FINAL_CLASSES = list(dict.fromkeys(UNIQUE_EXTENDED_CLASSES))


# Response model
class ClassificationResult(BaseModel):
    top_class: str
    confidence: float
    predictions: Dict[str, float]

    class Config:
        schema_extra = {
            "example": {
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
                    "textile": 0.00045594872790388763,
                },
            }
        }


@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "Garbage CLassifier API - Go to /api/docs for UI"}


# @app.post(
#     "/classify_bycats",
#     response_model=ClassificationResult,
#     tags=["Classification"],
#     summary="Classify garbage item",
#     description="Classify an image of garbage predefined categories",
#     responses={
#         200: {
#             "description": "Successful classification",
#             "content": {
#                 "application/json": {
#                     "example": {
#                         "top_class": "electronic waste",
#                         "confidence": 0.33171185851097107,
#                         "predictions": {
#                             "plastic bottle": 0.24136486649513245,
#                             "glass bottle": 0.0022902777418494225,
#                             "paper": 0.0015287415590137243,
#                             "cardboard": 0.0012100355233997107,
#                             "metal can": 0.24120794236660004,
#                             "organic waste": 0.18023031949996948,
#                             "electronic waste": 0.33171185851097107,
#                             "textile": 0.00045594872790388763,
#                         },
#                     }
#                 }
#             },
#         },
#         400: {"description": "Invalid input"},
#         500: {"description": "Internal server error"},
#     },
# )
# async def classify_bycats(
#     file: UploadFile = File(..., description="Image of garbage item"),
#     categories: str = Query(
#         default=",".join(DEFAULT_CLASSES),
#         description="Comma-separated classification categories",
#     ),
# ):
#     try:
#         # Process inputs
#         candidate_labels = [c.strip() for c in categories.split(",")]
#
#         image = load_image(await file.read())
#
#         # Run classification
#         results = classify_image(image, candidate_labels)
#
#         # Find top prediction
#         top_class = max(results, key=results.get)
#
#         return JSONResponse(
#             status_code=200,
#             content={
#                 "top_class": top_class,
#                 "confidence": results[top_class],
#                 "predictions": results,
#             },
#         )
#
#     except Exception as e:
#         logging.error(f"Classification error: {str(e)}")
#         return {"error": "Classification failed"}


@app.post(
    "/classify_predef_cat",
    response_model=ClassificationResult,
    tags=["Classification"],
    summary="Classify garbage item with predefined categories",
    description="Classify an image of garbage using all predefined categories from WASTE_DEFINITION.md",
    responses={
        200: {
            "description": "Successful classification",
            "content": {
                "application/json": {
                    "example": {
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
                            "textile": 0.00045594872790388763,
                        },
                    }
                }
            },
        },
        400: {"description": "Invalid input"},
        500: {"description": "Internal server error"},
    },
)
async def classify_predef_cat(
    file: UploadFile = File(..., description="Image of garbage item"),
):
    try:
        # Use predefined categories
        candidate_labels = FINAL_CLASSES

        image = load_image(await file.read())

        # Run classification
        results = classify_image(image, candidate_labels)

        # Find top prediction
        top_class = max(results, key=results.get)

        return JSONResponse(
            status_code=200,
            content={
                "top_class": top_class,
                "confidence": results[top_class],
                "predictions": results,
            },
        )

    except Exception as e:
        logging.error(f"Classification error: {str(e)}")
        return {"error": "Classification failed"}
