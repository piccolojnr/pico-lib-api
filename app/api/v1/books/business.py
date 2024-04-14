from flask_pyjwt import current_token
from app.utils.pagination import _pagination_nav_header_links, _pagination_nav_links
from app.models import (
    Book,
    User,
    Agent,
    Subject,
    Bookshelf,
    Language,
    Publisher,
    Bookmark,
)
from flask_restx import abort, marshal
from http import HTTPStatus
from app.services.recommendation_engine import generate_recommendations
from flask import jsonify, url_for, request
from app.api.v1.books.dto import book_pagination_model, book_model
from app import db
from app.utils.functions import add_resources
from app import auth_manager


def get_languages(language_ids):
    languages = []
    for language_id in language_ids:
        language = Language.query.filter_by(id=language_id).first()
        if language:
            languages.append(language)
    return languages


def get_publishers(publisher_ids):
    publishers = []
    for publisher_id in publisher_ids:
        publisher = Publisher.query.filter_by(id=publisher_id).first()
        if publisher:
            publishers.append(publisher)
    return publishers


def get_agents(agent_ids):
    agents = []
    for agent_id in agent_ids:
        agent = Agent.query.filter_by(id=agent_id).first()
        if agent:
            agents.append(agent)
    return agents


def get_subjects(subject_ids):
    subjects = []
    for subject_id in subject_ids:
        subject = Subject.query.filter_by(id=subject_id).first()
        if subject:
            subjects.append(subject)
    return subjects


def get_bookshelves(bookshelf_ids):
    bookshelves = []
    for bookshelf_id in bookshelf_ids:
        bookshelf = Bookshelf.query.filter_by(id=bookshelf_id).first()
        if bookshelf:
            bookshelves.append(bookshelf)
    return bookshelves


def process_create_book(data):
    agents = get_agents(data["agents"]) if "agents" in data else []
    bookshelves = get_bookshelves(data["bookshelves"]) if "bookshelves" in data else []
    languages = get_languages(data["languages"]) if "languages" in data else []
    resources = add_resources(data["resources"]) if "resources" in data else []
    subjects = get_subjects(data["subjects"]) if "subjects" in data else []
    publishers = get_publishers(data["publishers"]) if "publishers" in data else []
    data["agents"] = agents
    data["bookshelves"] = bookshelves
    data["languages"] = languages
    data["resources"] = resources
    data["subjects"] = subjects
    data["publishers"] = publishers

    for key, value in data.items():
        if value is None:
            del data[key]

    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    book_data = marshal(book, book_model)
    response = {
        "status": "success",
        "message": "Book created successfully",
        "item": book_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.book", book_id=book.id)}

    return response, response_status_code, response_headers


def process_delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return {"status": "success", "message": "Book deleted successfully"}
    else:
        abort(HTTPStatus.NOT_FOUND, "Book not found")


def process_update_book(book_id, data):
    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    for key, value in data.items():
        if value is not None and key not in ["id", "created_at", "updated_at"]:
            setattr(book, key, value)

    db.session.commit()
    return {
        "status": "success",
        "message": f"Book with ID {book_id} was successfully updated.",
    }


def process_get_books(
    page,
    per_page,
    lan=None,
    subject=None,
    agent=None,
    bookshelf=None,
    q=None,
    order=None,
    sort=None,
):
    filter_conditions = []
    if lan and lan != "all":
        filter_conditions.append(Book.languages.any(Language.code == lan))
    if q:
        filter_conditions.append(Book.title.ilike(f"%{q}%"))
    if subject:
        filter_conditions.append(Book.subjects.any(Subject.id == subject))
    if agent:
        filter_conditions.append(Book.agents.any(Agent.id == agent))
    if bookshelf:
        filter_conditions.append(Book.bookshelves.any(Bookshelf.id == bookshelf))
    if filter_conditions:
        books = Book.query.filter(*filter_conditions)
    else:
        books = Book.query

    if sort == "popularity":
        if order == "desc":
            books = books.order_by(Book.popularity_score.desc())
        else:
            books = books.order_by(Book.popularity_score.asc())
    elif sort == "downloads":
        if order == "desc":
            books = books.order_by(Book.downloads.desc())
        else:
            books = books.order_by(Book.downloads.asc())
    elif sort == "created_at":
        if order == "desc":
            books = books.order_by(Book.created_at.desc())
        else:
            books = books.order_by(Book.created_at.asc())
    elif sort == "updated_at":
        if order == "desc":
            books = books.order_by(Book.updated_at.desc())
        else:
            books = books.order_by(Book.updated_at.asc())
    elif sort == "title":
        if order == "desc":
            books = books.order_by(Book.title.desc())
        else:
            books = books.order_by(Book.title.asc())

    books = books.paginate(page=page, per_page=per_page)

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
    response_data["links"] = _pagination_nav_links(pagination, "books", lan=lan)
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(
        pagination, "books", lan=lan
    )
    response.headers["Total-Count"] = books.pages
    return response


def process_get_book(book_id):
    book = Book.query.filter(Book.id == book_id).first()

    if book:
        book_data = marshal(book, book_model)
        response = {
            "status": "success",
            "message": "Book found successfully",
            "item": book_data,
            "bookmark": {
                "bookmarked": False,
                "status": None,
            },
        }
        current_token = (
            request.headers["Authorization"].replace("Bearer ", "")
            if "Authorization" in request.headers
            else None
        )
        current_token = (
            auth_manager.convert_token(current_token) if current_token else None
        )
        public_id = current_token.sub["public_id"] if current_token else None
        if public_id:
            user: User = User.find_by_public_id(public_id)
            if user:
                user_id = user.id
                book_bookmark = Bookmark.query.filter(
                    Bookmark.user_id == user_id, Bookmark.book_id == book_id
                ).first()
                if book_bookmark:
                    response["item"]["bookmarked"] = True
                    response["item"]["bookmark_status"] = book_bookmark.status_str

        return response
    else:
        abort(HTTPStatus.NOT_FOUND, "Book not found")


def process_get_recommedations(page, per_page, lan):
    public_id = current_token.sub["public_id"]
    user: User = User.find_by_public_id(public_id)
    if user:
        recommendations, has_next, has_prev, total_pages = generate_recommendations(
            user, page, per_page, lan
        )
        pagination = dict(
            page=page,
            items_per_page=per_page,
            total_pages=total_pages,
            total_items=len(recommendations),
            items=recommendations,
            has_next=has_next,
            has_prev=has_prev,
            next_num=page + 1 if has_next else None,
            prev_num=page - 1 if has_prev else None,
            links=[],
        )
        response_data = marshal(pagination, book_pagination_model)
        response_data["links"] = _pagination_nav_links(
            pagination, "book_recommendations"
        )
        response = jsonify(response_data)
        response.headers["Link"] = _pagination_nav_header_links(
            pagination, "book_recommendations"
        )
        response.headers["Total-Count"] = total_pages
        return response_data
    else:
        abort(HTTPStatus.NOT_FOUND, "User not found")


def process_get_popular_books(page=1, per_page=10, lan="en"):
    filter_conditions = []

    if lan and lan != "all":
        filter_conditions.append(Book.languages.any(Language.code == lan))

    if filter_conditions:
        books = (
            Book.query.filter(*filter_conditions)
            .order_by(Book.popularity_score.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
    else:
        books = Book.query.order_by(Book.popularity_score.desc()).paginate(
            page=page, per_page=per_page, error_out=False
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
    response_data["links"] = _pagination_nav_links(pagination, "popular_books")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "popular_books")
    response.headers["Total-Count"] = books.total
    return response
