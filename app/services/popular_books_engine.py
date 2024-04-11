from app.services import (
    calculate_score,
    calculate_review_score,
    calculate_popularity_score,
)
from app.models import Book
from tqdm import tqdm


def preprocess_popularity_data():
    books = Book.query.all()
    for i in tqdm(range(len(books))):
        book = books[i]
        score = calculate_score(None, book)
        # Incorporate review score based on reviews and votes
        score += calculate_review_score(book)
        # Incorporate popularity score based on the number of reads
        score += calculate_popularity_score(book)
        book.popularity_score = score
