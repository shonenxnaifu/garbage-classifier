import io

from PIL import Image


def load_image(file) -> Image.Image:
    """Convert uploaded file to PIL Image"""
    image = Image.open(io.BytesIO(file)).convert("RGB")

    return image
