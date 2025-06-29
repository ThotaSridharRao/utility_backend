from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from uuid import uuid4
import shutil
import os
from utils.pdf_utils import (
    merge_pdfs, split_pdf_by_page_range,
    compress_pdf, images_to_pdf,
    pdf_to_images
)

router = APIRouter()

@router.post("/merge")
async def merge_pdf_files(files: list[UploadFile] = File(...)):
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="At least two PDF files are required to merge.")
    os.makedirs("static", exist_ok=True)
    temp_paths = []

    try:
        for f in files:
            temp_path = f"static/{uuid4()}_{f.filename}"
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(f.file, buffer)
            temp_paths.append(temp_path)

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

@router.post("/split")
async def split_pdf(file: UploadFile = File(...), start: int = Form(...), end: int = Form(...)):
    os.makedirs("static", exist_ok=True)
    input_path = f"static/{uuid4()}_{file.filename}"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_filename = f"{uuid4()}_split.pdf"
    output_path = f"static/{output_filename}"

    try:
        await split_pdf_by_page_range(input_path, output_path, start, end)
        return FileResponse(path=output_path, filename=output_filename, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

@router.post("/compress")
async def compress_pdf_file(file: UploadFile = File(...)):
    os.makedirs("static", exist_ok=True)
    input_path = f"static/{uuid4()}_{file.filename}"
    output_path = f"static/{uuid4()}_compressed.pdf"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        await compress_pdf(input_path, output_path)
        return FileResponse(path=output_path, filename=os.path.basename(output_path), media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

@router.post("/image-to-pdf")
async def convert_images_to_pdf(files: list[UploadFile] = File(...)):
    os.makedirs("static", exist_ok=True)
    output_path = f"static/{uuid4()}_converted.pdf"

    try:
        await images_to_pdf(files, output_path)
        return FileResponse(path=output_path, filename=os.path.basename(output_path), media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pdf-to-images")
async def convert_pdf_to_images(file: UploadFile = File(...)):
    os.makedirs("static", exist_ok=True)
    input_path = f"static/{uuid4()}_{file.filename}"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        output_files = await pdf_to_images(input_path)
        return {"images": output_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
