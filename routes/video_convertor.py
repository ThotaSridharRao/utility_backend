from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from utils.video_utils import convert_video_format
import os
import shutil
from uuid import uuid4

router = APIRouter()

@router.post("/convert")
async def convert_video(
    file: UploadFile = File(...),
    target_format: str = Form(...)
):
    allowed_formats = ['mp4', 'avi', 'mov', 'webm']
    if target_format.lower() not in allowed_formats:
        raise HTTPException(status_code=400, detail="Unsupported video format")

    try:
        os.makedirs("static", exist_ok=True)

        # === 📥 DEBUG LOGS ===
        print("📥 Received video for conversion:", file.filename)
        print("🎯 Target format:", target_format)

        # Save uploaded file temporarily
        temp_input_path = f"static/{uuid4()}_{file.filename}"
        with open(temp_input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Generate output filename and path
        output_filename = f"{uuid4()}.{target_format.lower()}"
        output_path = f"static/{output_filename}"

        # Convert using FFmpeg
        await convert_video_format(temp_input_path, output_path)

        # Log output size
        if os.path.exists(output_path):
            print(f"✅ Output file created: {output_filename}, Size: {os.path.getsize(output_path)} bytes")
        else:
            print(f"❌ Output file not created: {output_filename}")

        # Clean up input file
        os.remove(temp_input_path)

        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type=f"video/{target_format.lower()}"
        )

    except Exception as e:
        print("🔥 Conversion failed:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
