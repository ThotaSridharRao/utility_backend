from fastapi import FastAPI
from routes.image_convertor import router as image_converter_router
app = FastAPI(
    title="Utility Toolkit API",
    description="Backend API for Image Format Conversion and future media tools.",
    version="1.0.0"
)

# Register image conversion router
app.include_router(image_converter_router, prefix="/image", tags=["Image Tools"])
