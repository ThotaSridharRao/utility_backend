from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
import fitz  # PyMuPDF
import pikepdf
import os
import io

async def merge_pdfs(file_paths, output_path):
    merger = PdfMerger()
    for path in file_paths:
        merger.append(path)
    merger.write(output_path)
    merger.close()

async def split_pdf_by_page_range(input_path, output_path, start, end):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i in range(start - 1, end):
        if i < len(reader.pages):
            writer.add_page(reader.pages[i])
        else:
            raise ValueError("Page range is out of bounds.")

    with open(output_path, "wb") as f:
        writer.write(f)

async def compress_pdf(input_path, output_path):
    try:
        with pikepdf.open(input_path) as pdf:
            # Optimize and remove unused objects
            pdf.save(output_path, optimize_version=True)
    except Exception as e:
        raise RuntimeError(f"Compression failed: {str(e)}")

async def images_to_pdf(upload_files, output_path):
    image_list = []

    for upload_file in upload_files:
        contents = await upload_file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_list.append(image)

    if not image_list:
        raise ValueError("No valid images provided.")

    image_list[0].save(output_path, save_all=True, append_images=image_list[1:])

async def pdf_to_images(input_path):
    doc = fitz.open(input_path)
    image_paths = []

    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(dpi=200)
        image_path = f"static/page_{i + 1}.png"
        pix.save(image_path)
        image_paths.append(image_path)

    return image_paths
