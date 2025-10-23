from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Book Library API")

# Internal model
class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    year: int

# Response models
class BookSummary(BaseModel):
    title: str
    author: str

class BookDetail(BaseModel):
    id: int
    title: str
    author: str
    description: str
    year: int

# In-memory data store
books_db = [
    Book(id=1, title="1984", author="George Orwell", description="Dystopian novel.", year=1949),
    Book(id=2, title="The Hobbit", author="J.R.R. Tolkien", description="Fantasy adventure.", year=1937),
]

# Create a new book
@app.post("/books", response_model=BookDetail)
def create_book(book: Book):
    books_db.append(book)
    return book

# Read all books (summary view)
@app.get("/books", response_model=List[BookSummary])
def list_books():
    return [BookSummary(title=b.title, author=b.author) for b in books_db]

# Read single book (detail view)
@app.get("/books/{book_id}", response_model=BookDetail)
def get_book(book_id: int):
    for b in books_db:
        if b.id == book_id:
            return b
    raise HTTPException(status_code=404, detail="Book not found")

# Update existing book
@app.put("/books/{book_id}", response_model=BookDetail)
def update_book(book_id: int, updated: Book):
    for idx, b in enumerate(books_db):
        if b.id == book_id:
            books_db[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Book not found")

# Delete book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for idx, b in enumerate(books_db):
        if b.id == book_id:
            books_db.pop(idx)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

