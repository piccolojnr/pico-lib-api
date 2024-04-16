from app.models import (
    Book,
    User,
    Language,
    Bookmark,
)
from . import (
    calculate_score,
)  # Importing calculate_score function from the same directory
from sqlalchemy import desc


# Function to generate book recommendations for a user
def generate_recommendations(user: User, page=1, per_page=10, lan=None):
    # Query unread books for the user, optionally filtered by language
    if lan:
        unread_books = (
            Book.query.filter(~Book.bookmarks.any(Bookmark.user_id == user.id))
            .order_by(desc(Book.popularity_score))
            .limit(200)
            .all()
        )
    else:
        unread_books = (
            Book.query.filter(
                ~Book.bookmarks.any(Bookmark.user_id == user.id),
                Book.languages.any(Language.code == lan),  # Filter by language
            )
            .order_by(desc(Book.popularity_score))
            .limit(200)
            .all()
        )

    # Calculate scores for candidate books
    scores = {}
    for book in unread_books:
        score = calculate_score(user, book)
        scores[book] = score

    # Rank candidate books based on scores
    ranked_books = sorted(scores, key=scores.get, reverse=True)

    # Select books for the specified page
    start = (page - 1) * per_page
    end = start + per_page
    recommendations_page = ranked_books[start:end]

    # Determine pagination information
    has_next_page = len(ranked_books) - end > 0
    has_previous_page = page > 1
    total_pages = len(ranked_books) // per_page + 1

    # Return recommendations for the specified page along with pagination information
    return recommendations_page, has_next_page, has_previous_page, total_pages
