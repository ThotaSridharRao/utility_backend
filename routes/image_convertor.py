from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import os
from utils.image_utils import convert_image_format  # ✅ Correct import

from uuid import uuid4

router = APIRouter()

@router.post("/convert")
async def convert_image(
    file: UploadFile = File(...),
    target_format: str = Form(...)
):
    # Supported formats
    allowed_formats = ['jpg', 'jpeg', 'png', 'webp']
    if target_format.lower() not in allowed_formats:
        raise HTTPException(status_code=400, detail="Unsupported output format.")

    try:
        # Generate unique output file name
        output_filename = f"{uuid4()}.{target_format.lower()}"
        output_path = os.path.join("static", output_filename)

        # Convert the image using your utility function
        await convert_image_format(file, output_path, target_format)

        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type=f"image/{target_format}"
        )

    except Exception as e:
        print("🔥 Internal Server Error:", str(e))  # ✅ Add this line
        raise HTTPException(status_code=500, detail=str(e))

