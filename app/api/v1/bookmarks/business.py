from app.models import Book, Bookmark, BookmarkStatus, User
from flask_restx import abort, marshal
from http import HTTPStatus
from flask import jsonify, url_for
from app.utils.pagination import _pagination_nav_header_links, _pagination_nav_links
from .dto import (
    bookmark_model,
    bookmarks_pagination_model,
    bookmark_books_pagination_model,
    bookmark_book_model,
)
from app import db
from flask_pyjwt import current_token


def process_create_bookmark(book_id, status):
    public_id = current_token.sub["public_id"]

    book = Book.query.filter_by(id=book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, message=f"Book not found")

    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, message=f"User not found")

    existing_bookmark = Bookmark.query.filter(
        Bookmark.book_id == book_id, Bookmark.user_id == user.id
    ).first()
    if existing_bookmark:
        return process_update_bookmark(existing_bookmark.id, status)

    status = BookmarkStatus[status.upper()]

    bookmark = Bookmark(book_id=book_id, user_id=user.id, status=status)
    db.session.add(bookmark)
    db.session.commit()
    bookmark_data = marshal(bookmark, bookmark_model)
    response = {
        "status": "success",
        "message": "Bookmark created successfully",
        "item": bookmark_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.bookmarks", book_id=bookmark.id)}

    return response, response_status_code, response_headers


def process_delete_bookmark(book_id):
    public_id = current_token.sub["public_id"]
    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, message=f"User not found")

    book = Book.query.filter_by(id=book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, message=f"Book not found")

    bookmark = Bookmark.query.filter(
        Bookmark.book_id == book_id, Bookmark.user_id == user.id
    ).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return {"status": "success", "message": "Bookmark deleted successfully"}
    else:
        abort(HTTPStatus.NOT_FOUND, "Bookmark not found")


def process_update_bookmark(bookmark_id, status):
    public_id = current_token.sub["public_id"]
    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, message=f"User not found")

    bookmark = Bookmark.query.filter(
        Bookmark.id == bookmark_id, Bookmark.user_id == user.id
    ).first()
    if not bookmark:
        abort(HTTPStatus.NOT_FOUND, "Bookmark not found")

    if status:
        status = BookmarkStatus[status.upper()]
        bookmark.status = status

    db.session.commit()
    bookmark_data = marshal(bookmark, bookmark_model)
    response = {
        "status": "success",
        "message": "Bookmark updated successfully",
        "item": bookmark_data,
    }
    response_status_code = HTTPStatus.OK

    return response, response_status_code


def process_get_bookmark(bookmark_id):
    public_id = current_token.sub["public_id"]
    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, message=f"User not found")

    bookmark = Bookmark.query.filter(
        Bookmark.id == bookmark_id, Bookmark.user_id == user.id
    ).first()
    if bookmark:
        return bookmark
    else:
        abort(HTTPStatus.NOT_FOUND, "Bookmark not found")


def process_get_user_book_bookmark(book_id):
    public_id = current_token.sub["public_id"]
    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, message=f"User not found")

    bookmark = Bookmark.query.filter(
        Bookmark.book_id == book_id, Bookmark.user_id == user.id
    ).first()
    if bookmark:
        return bookmark
    else:
        abort(HTTPStatus.NOT_FOUND, "Bookmark not found")


def process_get_bookmarks(book_id, page=1, per_page=10):
    bookmarks = Bookmark.query.filter(Bookmark.book_id == book_id).paginate(
        page=page,
        per_page=per_page,
    )

    pagination = dict(
        page=bookmarks.page,
        items_per_page=bookmarks.per_page,
        total_pages=bookmarks.pages,
        total_items=bookmarks.total,
        items=bookmarks.items,
        has_next=bookmarks.has_next,
        has_prev=bookmarks.has_prev,
        next_num=bookmarks.next_num,
        prev_num=bookmarks.prev_num,
        links=[],
    )
    response_data = marshal(pagination, bookmarks_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "bookmarks")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "bookmarks")
    response.headers["Total-Count"] = bookmarks.pages
    return response


def process_get_bookmark_books(page=1, per_page=10, status=None):
    public_id = current_token.sub["public_id"]
    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, message=f"User not found")

    if status:
        status = BookmarkStatus[status.upper()]
        books = Book.query.filter(
            Book.bookmarks.any(Bookmark.user_id == user.id),
            Book.bookmarks.any(Bookmark.status == status),
        ).paginate(page=page, per_page=per_page)
    else:
        books = Book.query.filter(
            Book.bookmarks.any(Bookmark.user_id == user.id),
        ).paginate(page=page, per_page=per_page)

    pagination = dict(
        page=page,
        items_per_page=per_page,
        total_pages=books.pages,
        total_items=books.total,
        items=books.items,
        has_next=books.has_next,
        has_prev=books.has_prev,
        next_num=books.next_num,
        prev_num=books.prev_num,
        links=[],
    )
    response_data = marshal(pagination, bookmark_books_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "bookmark_books")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(
        pagination, "bookmark_books"
    )
    response.headers["Total-Count"] = books.total
    return response
