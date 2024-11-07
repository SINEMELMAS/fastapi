from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Kitap sınıfımızı oluşturuyoruz
class Book(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None  # Opsiyonel bir alan
    rating: Optional[float] = None     # Opsiyonel bir alan

# Veri deposu olarak bir kitap listesi kullanacağız (gerçek bir veritabanı yerine).
books = [
    Book(id=1, title="Sefiller", author="Victor Hugo", description="Bir klasik Fransız romanı", rating=9.0),
    Book(id=2, title="Suç ve Ceza", author="Fyodor Dostoevsky", description="Rus edebiyatının başyapıtlarından", rating=9.2),
]

# API Başlangıç rotası
@app.get("/")
def read_root():
    return {"message": "Kütüphane API'ye hoş geldiniz!"}

# Tüm kitapları listele
@app.get("/books", response_model=List[Book])
def get_books():
    return books

# ID'ye göre bir kitap getir
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Kitap bulunamadı")

# Yeni bir kitap ekle
@app.post("/books", response_model=Book)
def add_book(book: Book):
    if any(b.id == book.id for b in books):
        raise HTTPException(status_code=400, detail="Bu ID'ye sahip bir kitap zaten var.")
    books.append(book)
    return book

# Bir kitabı güncelle
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books):
        if book.id == book_id:
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Kitap bulunamadı")

# Bir kitabı sil
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            del books[i]
            return {"message": "Kitap silindi"}
    raise HTTPException(status_code=404, detail="Kitap bulunamadı")
