from app.models import Book, Language
from flask_restx import abort, marshal
from http import HTTPStatus
from flask import jsonify, url_for
from app.api.v1.books.dto import book_pagination_model
from app.utils.pagination import _pagination_nav_header_links, _pagination_nav_links
from .dto import langauge_model, languages_pagination_model
from app import db


def process_create_language(code, name):
    existing_lan = Language.query.filter(Language.code == code).first()
    if existing_lan:
        abort(HTTPStatus.FORBIDDEN, message=f"language with code {code} already exists")

    language = Language(code=code, name=name)
    db.session.add(language)
    db.session.commit()
    language_data = marshal(language, langauge_model)
    response = {
        "status": "success",
        "message": "Language created successfully",
        "item": language_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.languages", book_id=language.id)}

    return response, response_status_code, response_headers


def process_delete_language(language_id):
    language = Language.query.filter_by(id=language_id).first()
    if language:
        db.session.delete(language)
        db.session.commit()
        return {"status": "success", "message": "Language deleted successfully"}
    else:
        abort(HTTPStatus.NOT_FOUND, "Language not found")


def process_update_language(language_id, code, name):
    language = Language.query.filter(Language.id == language_id).first()
    if not language:
        abort(HTTPStatus.NOT_FOUND, "Language not found")

    if code:
        language.code = code

    if name:
        language.name = name

    db.session.commit()
    language_data = marshal(language, langauge_model)
    response = {
        "status": "success",
        "message": "Language updated successfully",
        "item": language_data,
    }
    response_status_code = HTTPStatus.OK

    return response, response_status_code


def process_get_language(language_id):
    language = Language.query.filter(Language.id == language_id).first()
    if language:
        return language
    else:
        abort(HTTPStatus.NOT_FOUND, "Language not found")


def process_get_languages(page=1, per_page=10):
    languages = Language.query.all()

    pagination = dict(
        items=languages,
        links=[],
    )
    response_data = marshal(pagination, languages_pagination_model)
    return response_data


def process_create_language_book(language_id, book_id):
    language = Language.query.filter_by(id=language_id).first()
    if not language:
        abort(HTTPStatus.NOT_FOUND, "Language not found")

    book = Book.query.filter_by(id=book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    language.books.append(book)

    db.session.commit()
    return {"status": "success", "message": "Book added to language successfully"}


def process_delete_language_book(language_id, user_public_id):
    language = Language.query.filter_by(id=language_id).first()
    if not language:
        abort(HTTPStatus.NOT_FOUND, "Language not found")

    book = Book.query.filter_by(id=user_public_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    language.books.remove(book)
    db.session.commit()

    return {
        "status": "success",
        "message": "Book removed from language successfully",
    }


def process_get_language_books(language_id, page=1, per_page=10):
    language = Language.query.filter(Language.id == language_id).first()
    if not language:
        abort(HTTPStatus.NOT_FOUND, "Language not found")
    books = Book.query.filter(Book.languages.any(Language.id == language.id)).paginate(
        page=page,
        per_page=per_page,
    )

    pagination = dict(
        page=books.page,
        items_per_page=books.per_page,
        total_pages=books.pages,
        total_items=books.total,
        items=books.items,
        has_next=books.has_next,
        has_prev=books.has_prev,
        next_num=books.next_num,
        prev_num=books.prev_num,
        links=[],
    )
    response_data = marshal(pagination, book_pagination_model)
    response_data["links"] = _pagination_nav_links(
        pagination,
        "language_books",
        language_id=language_id,
    )
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(
        pagination, "language_books", language_id=language_id
    )
    response.headers["Total-Count"] = books.pages
    return response
