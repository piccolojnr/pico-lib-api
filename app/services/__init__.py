from app.models import (
    Book,
    User,
    Bookmark,
    Comment,
    CommentType,
)
from sqlalchemy import func

from math import log1p

# Function to calculate review score for a book
def calculate_review_score(book: Book):
    # Query all reviews for the book
    reviews: list[Comment] = Comment.query.filter(
        Comment.book_id == book.id, Comment.type == CommentType.REVIEW
    ).all()
    
    total_score = 0
    total_votes = 0
    
    # Calculate total score and total votes based on reviews
    for review in reviews:
        total_score += review.rating * (
            review.upvotes() - review.downvotes()
        )  # Consider both rating and votes
        total_votes += review.upvotes() + review.downvotes()

    if total_votes > 0:
        return total_score / total_votes  # Calculate average score per vote
    else:
        return 0  # Default score if no reviews available

# Function to calculate popularity score for a book
def calculate_popularity_score(book: Book):
    # Get the maximum number of reads and downloads across all books
    max_reads = max(Bookmark.query.count(), 1)
    max_downloads = max(Book.query.with_entities(func.max(Book.downloads)).scalar(), 1)

    # Get the number of reads and downloads for the given book
    num_reads = max(Bookmark.query.filter(Bookmark.book_id == book.id).count(), 1)

    # Normalize reads and downloads to a 0-1 scale
    normalized_reads = log1p(num_reads) / log1p(max_reads)
    normalized_downloads = log1p(book.downloads) / log1p(max_downloads)

    # Calculate score based on normalized reads and downloads
    score = (5 * normalized_reads) + (5 * normalized_downloads)

    return score * 10  # Scale score to a 0-100 range

# Function to calculate a user's score for a book
def calculate_score(user: User, book: Book):
    score = 0
    
    # Example scoring function incorporating user's interests and book attributes
    for subject in book.subjects:
        if user and subject in user.subjects:
            score += 1
        score += subject.score  # Incorporate subject score into the score calculation

    for bookshelf in book.bookshelves:
        if user and bookshelf in user.bookshelves:
            score += 1
        score += bookshelf.score

    # Incorporate other factors into the score calculation, such as average rating
    if book.rating:
        score += book.rating

    return score
