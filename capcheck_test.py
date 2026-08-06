from transformers import pipeline
from PIL import Image
import os

print("Loading CapCheck model...")

detector = pipeline(
    "image-classification",
    model="capcheck/ai-human-generated-image-detection"
)

image_path = "test.jpg"

print("File exists:", os.path.exists(image_path))

img = Image.open(image_path)

result = detector(img)

print(result)