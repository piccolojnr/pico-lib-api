from sqlalchemy import or_
from flask_pyjwt import current_token
from app.models import (
    User,
    Book,
    Comment,
    CommentType,
    CommentVote,
    CommentVoteType,
    Rating,
)
from flask_restx import abort, marshal
from http import HTTPStatus
from app.utils.pagination import _pagination_nav_links, _pagination_nav_header_links
from flask import jsonify, url_for
from app.api.v1.comments.dto import (
    comment_model,
    comment_pagination_model,
)
from app import db


def process_user_comment_post(content, book_id, parent_id, comment_type, rating):
    public_id = current_token.sub["public_id"]
    user: User = User.find_by_public_id(public_id)

    if not content:
        abort(HTTPStatus.BAD_REQUEST, "Comment content is required")

    if not comment_type:
        abort(HTTPStatus.BAD_REQUEST, "Comment type is required")

    if type(comment_type) != str:
        abort(HTTPStatus.BAD_REQUEST, "Comment type must be a string")

    comment_type = comment_type.upper()

    if comment_type not in CommentType.__members__:
        abort(HTTPStatus.BAD_REQUEST, "Invalid comment type")

    comment_type = CommentType[comment_type]

    if not user:
        abort(HTTPStatus.NOT_FOUND, "User not found")

    if comment_type == CommentType.REPLY and not parent_id:
        abort(HTTPStatus.BAD_REQUEST, "Parent comment ID is required for replies")

    if book_id:
        book: Book = Book.get_by_id(book_id)
        if not book:
            abort(HTTPStatus.NOT_FOUND, "Book not found")
    else:
        if rating:
            exrating = Rating.query.filter_by(user_id=user.id).first()
            if exrating:
                exrating.rating = rating
                db.session.commit()
            else:
                new_rating = Rating(user_id=user.id, rating=rating, book_id=book_id)
                db.session.add(new_rating)
                db.session.commit()

    if parent_id:
        parent_comment: Comment = Comment.get_by_id(parent_id)
        if not parent_comment:
            abort(HTTPStatus.NOT_FOUND, "Parent comment not found")

    comment = Comment(
        content=content,
        user_id=user.id,
        book_id=book_id if book_id else None,
        parent_id=parent_id if parent_id else None,
        type=comment_type,
        rating=rating,
    )

    db.session.add(comment)
    db.session.commit()

    comment_data = marshal(comment, comment_model)
    response = {
        "status": "success",
        "message": f"New comment was successfully added: {content}.",
        "item": comment_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.comment", comment_id=comment.id)}

    return response, response_status_code, response_headers


def process_retrieve_user_comments(
    public_id,
    book_id,
    parent_id,
    comment_type,
    page=1,
    per_page=10,
):
    comment_type = comment_type.upper()

    if comment_type not in CommentType.__members__:
        abort(HTTPStatus.BAD_REQUEST, "Invalid comment type")

    if comment_type == CommentType.REPLY and not parent_id:
        abort(HTTPStatus.BAD_REQUEST, "Parent comment ID is required for replies")

    user_id = User.find_by_public_id(public_id).id if public_id else None

    query_filter = {
        "parent_id": parent_id,
        "user_id": user_id,
        "book_id": book_id,
        "type": comment_type,
    }
    query = Comment.query.filter_by(
        **{k: v for k, v in query_filter.items() if v}
    ).order_by(Comment.created_at.desc())

    comments_pagination = query.paginate(page=page, per_page=per_page)
    pagination = dict(
        page=comments_pagination.page,
        items_per_page=comments_pagination.per_page,
        total_pages=comments_pagination.pages,
        total_items=comments_pagination.total,
        items=comments_pagination.items,
        has_next=comments_pagination.has_next,
        has_prev=comments_pagination.has_prev,
        next_num=comments_pagination.next_num,
        prev_num=comments_pagination.prev_num,
        links=[],
    )
    response_data = marshal(pagination, comment_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "comments")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "comments")
    response.headers["Total-Count"] = comments_pagination.total

    return response


def process_retrieve_specific_comment(comment_id):
    comment = Comment.get_by_id(comment_id)
    if not comment:
        abort(HTTPStatus.NOT_FOUND, "Comment not found")
    return comment


def process_delete_comment(comment_id):
    comment = Comment.get_by_id(comment_id)
    if not comment:
        abort(HTTPStatus.NOT_FOUND, "Comment not found")
    db.session.delete(comment)
    db.session.commit()
    return {
        "status": "success",
        "message": f"Comment with ID {comment_id} was successfully deleted.",
    }


def process_update_comment(comment_id, content):
    comment = Comment.get_by_id(comment_id)
    if not comment:
        abort(HTTPStatus.NOT_FOUND, "Comment not found")
    if not content:
        abort(HTTPStatus.BAD_REQUEST, "Comment content is required")
    comment.content = content
    db.session.commit()
    return {
        "status": "success",
        "message": f"Comment with ID {comment_id} was successfully updated.",
    }


def process_vote_comment(comment_id, vote_type):
    comment = Comment.get_by_id(comment_id)
    if not comment:
        abort(HTTPStatus.NOT_FOUND, "Comment not found")
    public_id = current_token.sub["public_id"]
    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, "User not found")

    vote_type = vote_type.upper()
    if vote_type not in CommentVoteType.__members__:
        abort(HTTPStatus.BAD_REQUEST, "Invalid vote type")

    vote_type = CommentVoteType[vote_type]

    comment_vote = CommentVote.query.filter(
        CommentVote.comment_id == comment_id, CommentVote.user_id == user.id
    ).first()
    if comment_vote:
        if comment_vote.vote == vote_type:
            abort(HTTPStatus.BAD_REQUEST, "User already voted for this comment")
        else:
            db.session.delete(comment_vote)
            db.session.commit()

    comment_vote = CommentVote(comment_id=comment_id, user_id=user.id, vote=vote_type)
    db.session.add(comment_vote)
    db.session.commit()
    return jsonify(
        status="success",
        item=marshal(comment, comment_model),
        message=f"Comment with ID {comment_id} was successfully {vote_type}.",
    )
