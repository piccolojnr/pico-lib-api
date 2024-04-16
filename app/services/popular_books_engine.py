from app.services import (
    calculate_score,
    calculate_review_score,
    calculate_popularity_score,
)
from app.models import Book
from tqdm import tqdm

# Function to preprocess popularity data for books
def preprocess_popularity_data():
    # Retrieve all books from the database
    books = Book.query.all()
    
    # Iterate over each book
    for i in tqdm(range(len(books))):
        book = books[i]
        
        # Calculate the score for the book
        score = calculate_score(None, book)  # Example score calculation
        score += calculate_review_score(book)  # Incorporate review score
        score += calculate_popularity_score(book)  # Incorporate popularity score
        
        # Set the calculated popularity score for the book
        book.popularity_score = score
