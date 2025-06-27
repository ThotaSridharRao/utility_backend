from PIL import Image
import io
import os

def map_format(fmt: str) -> str:
    mapping = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "webp": "WEBP"
    }
    return mapping.get(fmt.lower(), fmt.upper())

async def convert_image_format(upload_file, output_path: str, target_format: str):
    # Ensure static folder exists
    os.makedirs("static", exist_ok=True)

    # Read the uploaded file content
    contents = await upload_file.read()

    # Load the image using Pillow
    img = Image.open(io.BytesIO(contents))

    # Convert and save using mapped format
    img.convert("RGB").save(output_path, format=map_format(target_format))
