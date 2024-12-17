from fastapi import FastAPI, Form, HTTPException

app = FastAPI()


@app.post("/profile/")
async def update_profile(
        username: str = Form(..., description="Kullanıcı adı (zorunlu)"),
        bio: str = Form(None, description="Kullanıcı biyografisi"),
        job: str = Form(None, description="Kullanıcının mesleği"),
        age: int = Form(None, description="Kullanıcının yaşı")
):
    # Girdi doğrulama
    if age is not None and age <= 0:
        raise HTTPException(status_code=400, detail="Yaş pozitif bir değer olmalıdır.")

    # Eksik alanlara varsayılan değerler atanabilir
    bio = bio or "Biyografi henüz eklenmedi."
    job = job or "Website belirtilmemiş."

    # Loglama veya veritabanı kaydı yapılabilir (örnek olarak bir loglama eklenmiştir)
    print(f"Kullanıcı profili güncellendi: {username}, Yaş: {age}")

    return {
        "message": "Profil başarıyla güncellendi!",
        "data": {
            "username": username,
            "bio": bio,
            "website": job,
            "age": age
        }
    }
