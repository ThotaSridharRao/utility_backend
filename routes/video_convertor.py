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

        # 📥 Save uploaded file
        temp_input_path = f"static/{uuid4()}_{file.filename}"
        with open(temp_input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🎯 Prepare output path
        output_filename = f"{uuid4()}.{target_format.lower()}"
        output_path = f"static/{output_filename}"

        # 🧠 Convert video
        await convert_video_format(temp_input_path, output_path)

        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Video conversion failed")

        os.remove(temp_input_path)  # 🧹 Cleanup input

        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type=f"video/{target_format.lower()}"
        )

    except Exception as e:
        print("🔥 Conversion failed:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
