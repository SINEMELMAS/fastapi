from fastapi import FastAPI, UploadFile, HTTPException

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    allowed_types = ["image/png", "image/jpeg", "application/pdf"]
    max_file_size = 5 * 1024 * 1024  # 5 MB

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Dosya türü desteklenmiyor.")

    # Dosya boyutunu kontrol etme
    file_data = await file.read()
    if len(file_data) > max_file_size:
        raise HTTPException(status_code=400, detail="Dosya boyutu 5 MB'yi aşamaz.")

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(file_data)
    }
