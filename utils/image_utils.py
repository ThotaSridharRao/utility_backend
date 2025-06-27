from PIL import Image
import io

async def convert_image_format(upload_file, output_path: str, target_format: str):
    import os

    # Ensure static folder exists
    os.makedirs("static", exist_ok=True)

    # Read the uploaded file content
    contents = await upload_file.read()

    # Load the image using Pillow
    img = Image.open(io.BytesIO(contents))

    # Convert and save
    img.convert("RGB").save(output_path, format=target_format.upper())
