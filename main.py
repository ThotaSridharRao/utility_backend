from fastapi import FastAPI
from routes.image_convertor import router as image_converter_router
from routes.video_convertor import router as video_converter_router
from routes.color_palette import router as color_palette_router
from fastapi.middleware.cors import CORSMiddleware
from routes.pdf_tools import router as pdf_tools_router

app = FastAPI(
    title="Utility Toolkit API",
    description="Backend API for Image Format Conversion and future media tools.",
    version="1.0.0"
)

# ✅ Add middleware AFTER app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://webdevutility.onrender.com"],  # your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register image conversion router
app.include_router(image_converter_router, prefix="/image", tags=["Image Tools"])
app.include_router(video_converter_router, prefix="/video", tags=["Video Tools"])
app.include_router(color_palette_router, prefix="/color", tags=["Color Tools"])
app.include_router(pdf_tools_router, prefix="/pdf", tags=["PDF Tools"])
