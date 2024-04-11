import datetime
from app.models import Book, Resource
from flask_restx import abort, marshal
from http import HTTPStatus
from flask import jsonify, url_for

from app.utils.pagination import _pagination_nav_header_links, _pagination_nav_links
from .dto import resource_model, resources_pagination_model
from app import db
from app.utils.functions import add_resource_type


def process_create_resource(book_id, data):
    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")
    data["book"] = book
    new_resource = Resource.query.filter(Resource.url == data["url"]).first()
    if new_resource:
        abort(HTTPStatus.CONFLICT, "Resource already exists")

    resource_type = add_resource_type(data["type"])
    data["type"] = resource_type
    modified = (
        datetime.datetime.fromisoformat(data["modified"]) if data["modified"] else None
    )
    data["modified"] = modified
    resource = Resource(**data)
    db.session.add(resource)
    db.session.commit()
    resource_data = marshal(resource, resource_model)
    response = {
        "status": "success",
        "message": "Resource created successfully",
        "item": resource_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.resources", book_id=resource.id)}

    return response, response_status_code, response_headers


def process_delete_resource(resource_id):
    resource = Resource.query.filter_by(id=resource_id).first()
    if resource:
        db.session.delete(resource)
        db.session.commit()
        return {"status": "success", "message": "Resource deleted successfully"}
    else:
        abort(HTTPStatus.NOT_FOUND, "Resource not found")


def process_update_resource(resource_id, data):
    resource = Resource.query.filter(Resource.id == resource_id).first()
    if not resource:
        abort(HTTPStatus.NOT_FOUND, "Resource not found")

    for key, value in data.items():
        if value is not None and key not in ["id"]:
            if key == "type":
                resource_type = add_resource_type(value)
                value = resource_type
            elif key == "modified":
                modified = datetime.datetime.fromisoformat(value) if value else None
                value = modified
            setattr(resource, key, value)

    db.session.commit()
    resource_data = marshal(resource, resource_model)
    response = {
        "status": "success",
        "message": "Resource updated successfully",
        "item": resource_data,
    }
    response_status_code = HTTPStatus.OK

    return response, response_status_code


def process_get_resource(resource_id):
    resource = Resource.query.filter(Resource.id == resource_id).first()
    if resource:
        return resource
    else:
        abort(HTTPStatus.NOT_FOUND, "Resource not found")


def process_get_resources(book_id, page=1, per_page=10):
    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")
    resources = Resource.query.filter(Resource.book_id == book_id).paginate(
        page=page,
        per_page=per_page,
    )

    pagination = dict(
        page=resources.page,
        items_per_page=resources.per_page,
        total_pages=resources.pages,
        total_items=resources.total,
        items=resources.items,
        has_next=resources.has_next,
        has_prev=resources.has_prev,
        next_num=resources.next_num,
        prev_num=resources.prev_num,
        links=[],
    )
    response_data = marshal(pagination, resources_pagination_model)
    response_data["links"] = _pagination_nav_links(
        pagination, "resources", book_id=book_id
    )
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(
        pagination, "resources", book_id=book_id
    )
    response.headers["Total-Count"] = resources.pages
    return response
