from http import HTTPStatus
from flask_restx import abort, marshal
from app import db
from flask import jsonify, url_for
from app.models import Agent, AgentType, Book
from app.utils.pagination import _pagination_nav_header_links, _pagination_nav_links
from app.api.v1.agents.dto import agent_pagination_model, agent_model


# Process creation of an agent
def process_create_agent(data):
    # Convert agent type to uppercase and get the corresponding AgentType enum value
    data["type"] = AgentType[data["type"].upper()] if data["type"] else None
    # Set default agent type to OTHER if not specified
    data["type"] = AgentType.OTHER if data["type"] == None else data["type"]

    # Create agent object and add it to the database
    agent = Agent(**data)
    db.session.add(agent)
    db.session.commit()
    agent_data = marshal(agent, agent_model)
    response = {
        "status": "success",
        "message": "Agent created successfully",
        "item": agent_data,
    }
    response_status_code = HTTPStatus.CREATED
    response_headers = {"Location": url_for("api.agent", agent_id=agent.id)}

    return response, response_status_code, response_headers


# Process retrieval of an agent
def process_get_agent(agent_id):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "Agent not found")
    return marshal(agent, agent_model)


# Process updating an agent
def process_update_agent(agent_id, data):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "Agent not found")

    for key, value in data.items():
        if value is not None and key != "id":
            if key == "type":
                value = AgentType[value.upper()]
            setattr(agent, key, value)

    db.session.commit()
    return {
        "status": "success",
        "message": f"Agent with ID {agent_id} was successfully updated.",
    }


# Process deletion of an agent
def process_delete_agent(agent_id):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "agent not found")
    db.session.delete(agent)
    db.session.commit()
    return {"status": "success", "message": "agent deleted successfully"}


# Process retrieval of agents with pagination and filtering
def process_get_agents(page=1, per_page=10, type=None, q=None):

    filter_conditions = []
    if q:
        filter_conditions.append(Agent.name.ilike(f"%{q}%"))
    if type and type != "all":
        agent_type = AgentType[type.upper()]
        filter_conditions.append(Agent.type == agent_type)

    if filter_conditions:
        agents = Agent.query.filter(*filter_conditions).paginate(
            page=page, per_page=per_page, error_out=False
        )
    else:
        agents = Agent.query.paginate(page=page, per_page=per_page)

    pagination = dict(
        page=agents.page,
        items_per_page=agents.per_page,
        total_pages=agents.pages,
        total_items=agents.total,
        items=agents.items,
        has_next=agents.has_next,
        has_prev=agents.has_prev,
        next_num=agents.next_num,
        prev_num=agents.prev_num,
        links=[],
    )
    response_data = marshal(pagination, agent_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "agents")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination, "agents")
    response.headers["Total-Count"] = agents.pages
    return response


# Process retrieval of popular agents with pagination
def process_get_popular_agents(page=1, per_page=10):
    agents = Agent.query.filter(
        Agent.type == AgentType.AUTHOR, Agent.books.any(Book.downloads > 20)
    ).paginate(page=page, per_page=per_page, error_out=False)

    pagination = dict(
        page=agents.page,
        items_per_page=agents.per_page,
        total_pages=agents.pages,
        total_items=agents.total,
        items=agents.items,
        has_next=agents.has_next,
        has_prev=agents.has_prev,
        next_num=agents.next_num,
        prev_num=agents.prev_num,
        links=[],
    )
    response_data = marshal(pagination, agent_pagination_model)
    response_data["links"] = _pagination_nav_links(pagination, "popular_agents")
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(
        pagination, "popular_agents"
    )
    response.headers["Total-Count"] = agents.pages
    return response


# Process adding a book to an agent
def process_add_agent_book(agent_id, book_id):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "Agent not found")

    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    if book in agent.books:
        abort(HTTPStatus.CONFLICT, "Book already assigned to agent")

    agent.books.append(book)
    db.session.commit()
    return {"status": "success", "message": "Book added successfully"}


# Process removing a book from an agent
def process_remove_agent_book(agent_id, book_id):
    agent = Agent.query.filter(Agent.id == agent_id).first()
    if not agent:
        abort(HTTPStatus.NOT_FOUND, "Agent not found")

    book = Book.query.filter(Book.id == book_id).first()
    if not book:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    if book not in agent.books:
        abort(HTTPStatus.NOT_FOUND, "Book not found")

    agent.books.remove(book)
    db.session.commit()
    return {"status": "success", "message": "Book removed successfully"}
