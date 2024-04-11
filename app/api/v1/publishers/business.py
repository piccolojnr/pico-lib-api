from app.models import Book, Publisher
from flask_restx import abort, marshal
from http import HTTPStatus
from flask import jsonify, url_for
from app.api.v1.books.dto import book_pagination_model
from app.utils.pagination import _pagination_nav_header_links, _pagination_nav_links
from .dto import publisher_model, publishers_pagination_model
from app import db


def process_create_publisher(name):
    existing_lan = Publisher.query.filter(Publisher.name == name).first()
    if existing_lan:
        abort(
            HTTPStatus.FORBIDDEN, message=f"publisher with name {name} already exists"
        )

    publisher = Publisher(name=name)
    db.session.add(publisher)
    db.session.commit()
    publisher_data = marshal(publisher, publisher_model)
    response = {
        "status": "success",
        "message": "Publisher created successfully",
        "item": publisher_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.publishers", book_id=publisher.id)}

    return response, response_status_code, response_headers


def process_delete_publisher(publisher_id):
    publisher = Publisher.query.filter_by(id=publisher_id).first()
    if publisher:
        db.session.delete(publisher)
        db.session.commit()
        return {"status": "success", "message": "Publisher deleted successfully"}
    else:
        abort(HTTPStatus.NOT_FOUND, "Publisher not found")


def process_update_publisher(publisher_id, name):
    publisher = Publisher.query.filter(Publisher.id == publisher_id).first()
    if not publisher:
        abort(HTTPStatus.NOT_FOUND, "Publisher not found")

    if name:
        publisher.name = name

    db.session.commit()
    publisher_data = marshal(publisher, publisher_model)
    response = {
        "status": "success",
        "message": "Publisher updated successfully",
        "item": publisher_data,
    }
    response_status_code = HTTPStatus.OK

    return response, response_status_code


def process_get_publisher(publisher_id):
    publisher = Publisher.query.filter(Publisher.id == publisher_id).first()
    if publisher:
        return publisher
    else:
        abort(HTTPStatus.NOT_FOUND, "Publisher not found")


def process_get_publishers(page=1, per_page=10):
    publishers = Publisher.query.paginate(
        page=page,
        per_page=per_page,
    )

    pagination = dict(
        page=publishers.page,
        items_per_page=publishers.per_page,
        total_pages=publishers.pages,
        total_items=publishers.total,
        items=publishers.items,
        has_next=publishers.has_next,
        has_prev=publishers.has_prev,
        next_num=publishers.next_num,
        prev_num=publishers.prev_num,
        links=[],
    )
    response_data = marshal(pagination, publishers_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "publishers")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "publishers")
    response.headers["Total-Count"] = publishers.pages
    return response


def process_create_publisher_book(publisher_id, book_id):
    publisher = Publisher.query.filter_by(id=publisher_id).first()
    if not publisher:
        abort(HTTPStatus.NOT_FOUND, "Publisher not found")

    book = Book.query.filter_by(id=book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    publisher.books.append(book)

    db.session.commit()
    return {"status": "success", "message": "Book added to publisher successfully"}


def process_delete_publisher_book(publisher_id, user_public_id):
    publisher = Publisher.query.filter_by(id=publisher_id).first()
    if not publisher:
        abort(HTTPStatus.NOT_FOUND, "Publisher not found")

    book = Book.query.filter_by(id=user_public_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    publisher.books.remove(book)
    db.session.commit()

    return {
        "status": "success",
        "message": "Book removed from publisher successfully",
    }


def process_get_publisher_books(publisher_id, page=1, per_page=10):
    publisher = Publisher.query.filter(Publisher.id == publisher_id).first()
    if not publisher:
        abort(HTTPStatus.NOT_FOUND, "Publisher not found")
    books = Book.query.filter(
        Book.publishers.any(Publisher.id == publisher.id)
    ).paginate(
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
        pagination, "publisher_books", publisher_id=publisher_id
    )
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(
        pagination, "publisher_books", publisher_id=publisher_id
    )
    response.headers["Total-Count"] = books.pages
    return response
