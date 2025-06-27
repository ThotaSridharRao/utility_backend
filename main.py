from fastapi import FastAPI
from routes.image_convertor import router as image_converter_router
from routes.video_convertor import router as video_converter_router
from fastapi.middleware.cors import CORSMiddleware

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
