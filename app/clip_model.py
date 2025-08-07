import torch
from transformers import CLIPModel, CLIPProcessor

# Load model once at startup
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def classify_image(image, candidate_labels):
    """Run zero-shot classification"""
    inputs = processor(
        text=candidate_labels, images=image, return_tensors="pt", padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # Calculate probabilities
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]

    return {label: float(prob) for label, prob in zip(candidate_labels, probs)}

