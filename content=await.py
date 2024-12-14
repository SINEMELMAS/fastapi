import os
import logging
from fastapi import FastAPI, UploadFile, HTTPException

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Yükleme dizini
UPLOAD_DIR = "uploaded_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# FastAPI uygulaması
app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    """
    Dosya yükleme endpoint'i. Dosya yüklenir, boyut ve tür kontrol edilir.
    Yüklenen dosya sunucuda kaydedilir.
    """
    try:
        # Desteklenen dosya türleri ve maksimum boyut
        allowed_types = ["text/plain", "image/png", "image/jpeg"]
        max_size = 5 * 1024 * 1024  # 5 MB

        # Dosya türü kontrolü
        if file.content_type not in allowed_types:
            logging.warning(f"Desteklenmeyen dosya türü: {file.content_type}")
            raise HTTPException(status_code=400, detail="Desteklenmeyen dosya türü.")

        # Dosya içeriğini oku
        content = await file.read()

        # Dosya boyutu kontrolü
        if len(content) > max_size:
            logging.warning(f"Dosya boyutu sınırı aşıldı: {len(content)} bayt")
            raise HTTPException(status_code=400, detail="Dosya boyutu 5 MB'yi aşamaz.")

        # Dosyayı kaydet
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)

        logging.info(f"Dosya başarıyla yüklendi: {file.filename} ({len(content)} bayt)")

        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "saved_path": file_path
        }

    except HTTPException as e:
        # Hata durumlarını logla ve ilet
        logging.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        # Beklenmeyen hatalar için log ve hata yanıtı
        logging.error(f"Beklenmeyen bir hata oluştu: {str(e)}")
        raise HTTPException(status_code=500, detail="Bir hata oluştu.")
