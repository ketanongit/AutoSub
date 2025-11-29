from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
import os
import sys
import uuid
from typing import Optional, Dict, Any

from .subtitle_generator import SubtitleGenerator

app = FastAPI(title="AutoSub API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Models
class BurnRequest(BaseModel):
    video_filename: str
    srt_content: str
    style_config: Dict[str, Any]

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        # Generate unique filename to prevent collisions
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"filename": unique_filename, "original_name": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcribe")
async def transcribe_video(filename: str = Body(..., embed=True), model: str = Body("base", embed=True)):
    video_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    try:
        generator = SubtitleGenerator(whisper_model=model)
        
        # Extract audio and transcribe
        temp_audio = f"temp_{uuid.uuid4()}.wav"
        generator.extract_audio(video_path, temp_audio)
        result = generator.transcribe_audio(temp_audio)
        
        # Cleanup audio
        if os.path.exists(temp_audio):
            os.remove(temp_audio)
            
        return {"segments": result["segments"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/burn")
async def burn_subtitles(request: BurnRequest):
    video_path = os.path.join(UPLOAD_DIR, request.video_filename)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
        
    try:
        # Create temporary SRT file
        srt_filename = f"{uuid.uuid4()}.srt"
        srt_path = os.path.join(OUTPUT_DIR, srt_filename)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(request.srt_content)
            
        # Generate output video path
        output_filename = f"final_{request.video_filename}"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        generator = SubtitleGenerator()
        generator.add_subtitles_to_video_with_srt(
            video_path, 
            srt_path, 
            output_path, 
            style_config=request.style_config
        )
        
        # Cleanup SRT
        if os.path.exists(srt_path):
            os.remove(srt_path)
            
        return {"output_filename": output_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/outputs/{filename}")
async def get_output_video(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

@app.get("/uploads/{filename}")
async def get_uploaded_video(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
