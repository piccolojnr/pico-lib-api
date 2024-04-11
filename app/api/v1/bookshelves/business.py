from flask_restx import marshal
from app.models import User, Bookshelf, Book
from app import db
from flask import jsonify, url_for
from flask_restx import abort
from http import HTTPStatus
from .dto import bookshelf_model, bookshelf_pagination_model
from flask_pyjwt import current_token
from app.utils.pagination import _pagination_nav_header_links, _pagination_nav_links
from sqlalchemy import desc


def process_create_bookshelf(data):
    public_id = current_token.sub["public_id"]

    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, "user not found")

    data["user_id"] = user.id

    bookshelf = Bookshelf(**data)
    db.session.add(bookshelf)
    db.session.commit()
    bookshelf_data = marshal(bookshelf, bookshelf_model)
    response = {
        "status": "success",
        "message": "Bookshelf created successfully",
        "item": bookshelf_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.bookshelf", bookshelf_id=bookshelf.id)}

    return response, response_status_code, response_headers


def process_get_bookshelf(bookshelf_id):
    bookshelf = Bookshelf.query.filter(Bookshelf.id == bookshelf_id).first()
    if not bookshelf:
        abort(HTTPStatus.NOT_FOUND, "Bookshelf not found")

    return marshal(bookshelf, bookshelf_model)


def process_update_bookshelf(bookshelf_id, data):
    public_id = current_token.sub["public_id"]
    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, "user not found")
    bookshelf = Bookshelf.query.filter(
        Bookshelf.id == bookshelf_id, Bookshelf.user_id == user.id
    ).first()
    if not bookshelf:
        abort(HTTPStatus.NOT_FOUND, "Bookshelf not found")

    for key, value in data.items():
        if value is not None and key != "id":
            setattr(bookshelf, key, value)

    db.session.commit()
    return {
        "status": "success",
        "message": f"bookshelf with ID {bookshelf_id} was successfully updated.",
    }


def process_delete_bookshelf(bookshelf_id):
    public_id = current_token.sub["public_id"]
    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, "user not found")

    bookshelf = Bookshelf.query.filter(
        Bookshelf.id == bookshelf_id, Bookshelf.user_id == user.id
    ).first()
    if not bookshelf:
        abort(HTTPStatus.NOT_FOUND, "Bookshelf not found")

    db.session.delete(bookshelf)
    db.session.commit()

    return {
        "status": "success",
        "message": f"bookshelf with ID {bookshelf_id} was successfully deleted.",
    }


def process_get_bookshelves(page=1, per_page=10, q=None):
    filter_conditions = []
    if q:
        filter_conditions.append(Bookshelf.name.ilike(f"%{q}%"))
    if filter_conditions:
        bookshelves = (
            Bookshelf.query.filter(Bookshelf.is_public == True, *filter_conditions)
            .order_by(desc(Bookshelf.score))
            .paginate(page=page, per_page=per_page)
        )
    else:
        bookshelves = (
            Bookshelf.query.filter(Bookshelf.is_public == True)
            .order_by(desc(Bookshelf.score))
            .paginate(page=page, per_page=per_page)
        )
    pagination = dict(
        page=bookshelves.page,
        items_per_page=bookshelves.per_page,
        total_pages=bookshelves.pages,
        total_items=bookshelves.total,
        items=bookshelves.items,
        has_next=bookshelves.has_next,
        has_prev=bookshelves.has_prev,
        next_num=bookshelves.next_num,
        prev_num=bookshelves.prev_num,
        links=[],
    )
    response_data = marshal(pagination, bookshelf_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "bookshelves")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "bookshelves")
    response.headers["Total-Count"] = bookshelves.pages
    return response


def process_get_bookshelves_by_user(user_id, page=1, per_page=10):
    public_id = current_token.sub["public_id"]
    get_public_only = True
    if public_id:
        user = User.find_by_public_id(public_id)
        if user:
            if user_id == user.id:
                get_public_only = False

    if get_public_only:
        bookshelves = Bookshelf.query.filter(
            Bookshelf.user_id == user_id,
            Bookshelf.public == True,
        ).paginate(page=page, per_page=per_page)
    else:
        bookshelves = Bookshelf.query.filter(
            Bookshelf.user_id == user_id,
        ).paginate(page=page, per_page=per_page)
    pagination = dict(
        page=bookshelves.page,
        items_per_page=bookshelves.per_page,
        total_pages=bookshelves.pages,
        total_items=bookshelves.total,
        items=bookshelves.items,
        has_next=bookshelves.has_next,
        has_prev=bookshelves.has_prev,
        next_num=bookshelves.next_num,
        prev_num=bookshelves.prev_num,
        links=[],
    )
    response_data = marshal(pagination, bookshelf_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "bookshelves")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "bookshelves")
    response.headers["Total-Count"] = bookshelves.pages
    return response


def process_create_bookshelf_book_relationship(bookshelf_id, book_id):
    bookshelf = Bookshelf.query.filter(Bookshelf.id == bookshelf_id).first()
    if not bookshelf:
        abort(HTTPStatus.NOT_FOUND, "Bookshelf not found")

    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    bookshelf.books.append(book)
    db.session.commit()
    return {"status": "success", "message": "Book added successfully"}


def process_delete_bookshelf_book_relationship(bookshelf_id, book_id):
    bookshelf = Bookshelf.query.filter(Bookshelf.id == bookshelf_id).first()
    if not bookshelf:
        abort(HTTPStatus.NOT_FOUND, "Bookshelf not found")

    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    bookshelf.books.remove(book)
    db.session.commit()
    return {"status": "success", "message": "Book removed successfully"}
