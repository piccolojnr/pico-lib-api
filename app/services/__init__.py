from app.models import (
    Book,
    User,
    Bookmark,
    Comment,
    CommentType,
)
from sqlalchemy import func

from math import log1p


def calculate_review_score(book: Book):
    reviews: list[Comment] = Comment.query.filter(
        Comment.book_id == book.id, Comment.type == CommentType.REVIEW
    ).all()
    total_score = 0
    total_votes = 0
    for review in reviews:
        total_score += review.rating * (
            review.upvotes() - review.downvotes()
        )  # Consider both rating and svotes
        total_votes += review.upvotes() + review.downvotes()

    if total_votes > 0:
        return total_score / total_votes  # Calculate average score per vote
    else:
        return 0  # Default score if no reviews available


def calculate_popularity_score(book: Book):
    max_reads = max(Bookmark.query.count(), 1)
    num_reads = max(Bookmark.query.filter(Bookmark.book_id == book.id).count(), 1)
    max_downloads = max(Book.query.with_entities(func.max(Book.downloads)).scalar(), 1)

    # Normalize reads and downloads to a 0-1 scale
    normalized_reads = log1p(num_reads) / log1p(max_reads)
    normalized_downloads = log1p(book.downloads) / log1p(max_downloads)

    # Calculate score
    score = (5 * normalized_reads) + (5 * normalized_downloads)

    return score * 10


def calculate_score(user: User, book: Book):
    # Example scoring function
    score = 0
    for subject in book.subjects:
        score = 0
        if user:
            if subject in user.subjects:
                score += 1

        score += subject.score  # Incorporate subject score into the score calculation

    for bookshelf in book.bookshelves:
        score = 0
        if user:
            if bookshelf in user.bookshelves:
                score += 1
        score += bookshelf.score

    # Incorporate other factors into the score calculation, such as average rating
    if book.rating:
        score += book.rating

    return score
