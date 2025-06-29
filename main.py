from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from routes.image_convertor import router as image_converter_router
from routes.video_convertor import router as video_converter_router
from routes.color_palette import router as color_palette_router
from routes.pdf_tools import router as pdf_tools_router

# Initialize app
app = FastAPI(
    title="Utility Toolkit API",
    description="Backend API for image, video, color palette, and PDF tools.",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://webdevutility.onrender.com"],  # Frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(image_converter_router, prefix="/image", tags=["Image Tools"])
app.include_router(video_converter_router, prefix="/video", tags=["Video Tools"])
app.include_router(color_palette_router, prefix="/color", tags=["Color Tools"])
app.include_router(pdf_tools_router, prefix="/pdf", tags=["PDF Tools"])
