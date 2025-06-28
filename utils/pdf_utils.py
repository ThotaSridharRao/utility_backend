from PyPDF2 import PdfMerger
import os

async def merge_pdfs(pdf_paths: list, output_path: str):
    merger = PdfMerger()
    for path in pdf_paths:
        merger.append(path)
    with open(output_path, 'wb') as f_out:
        merger.write(f_out)
    merger.close()
