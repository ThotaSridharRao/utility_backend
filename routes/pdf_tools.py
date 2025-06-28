from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from uuid import uuid4
import shutil
import os
from utils.pdf_utils import merge_pdfs

router = APIRouter()

@router.post("/merge")
async def merge_pdf_files(files: list[UploadFile] = File(...)):
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="At least two PDF files are required to merge.")

    os.makedirs("static", exist_ok=True)
    temp_paths = []

    try:
        # Save files temporarily
        for f in files:
            temp_path = f"static/{uuid4()}_{f.filename}"
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(f.file, buffer)
            temp_paths.append(temp_path)

        # Output file path
        output_filename = f"{uuid4()}_merged.pdf"
        output_path = f"static/{output_filename}"

        await merge_pdfs(temp_paths, output_path)

        return FileResponse(path=output_path, filename=output_filename, media_type="application/pdf")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        for path in temp_paths:
            if os.path.exists(path):
                os.remove(path)
