from fastapi import FastAPI, UploadFile
from fastapi import HTTPException
app = FastAPI()

# Example 1: Reading text file
@app.post("/upload-text/")
async def upload_text(file: UploadFile):
  content = await file.read()
  text_content = content.decode('utf-8')  # Convert bytes to string
  return {"text": text_content}

# Example 2: Reading image file
@app.post("/upload-image/")
async def upload_image(file: UploadFile):
  content = await file.read()
  # Process image bytes
  return {"file_size": len(content)}

# Example 3: Reading with size limit
@app.post("/upload-limited/")
async def upload_limited(file: UploadFile):
  content = await file.read()
  if len(content) > 1_000:  # 1MB limit
      raise HTTPException(status_code=400, detail="File too large")
  return {"file_size": len(content)}