from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.color_utils import extract_palette

router = APIRouter()

@router.post("/extract")
async def extract_color_palette(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image.")

        contents = await file.read()
        palette = extract_palette(contents)

        return {
            "message": "Palette extracted successfully.",
            "dominant_color": palette["dominant"],
            "palette": palette["palette"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
