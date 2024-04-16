import datetime
from app import db
from app.models import (
    Agent,
    Resource,
    ResourceType,
    AgentType,
    Bookshelf,
    Language,
    Subject,
)
from app.models.publishers import Publisher


# Function to add a new resource type to the database if it doesn't exist
def add_resource_type(resource_type):
    new_type = ResourceType.query.filter(ResourceType.name == resource_type).first()
    if not new_type:
        new_type = ResourceType(name=resource_type)
        db.session.add(new_type)
    return new_type


# Function to add new resources to the database
def add_resources(resources):
    new_resources = []
    for resource in resources:
        resource_type = resource["type"]
        if resource_type:
            new_type = add_resource_type(resource_type)
        url = resource["url"]
        size = resource["size"]

        if "modified" in resource.keys():
            modified = datetime.datetime.fromisoformat(resource["modified"])
        else:
            modified = None

        new_resource = Resource.query.filter(Resource.url == url).first()
        if not new_resource:
            new_resource = Resource(
                url=url, size=size, type_name=new_type.name, modified=modified
            )
            db.session.add(new_resource)
        new_resources.append(new_resource)
    return new_resources


# Function to add new agents (e.g., authors) to the database
def add_agents(agents):
    new_agents = []
    for agent in agents:
        type = agent["type"]
        new_type = AgentType[type] if type else AgentType.OTHER
        name = agent["name"]
        alias = agent["alias"]
        birth_date = agent["birth_date"]
        death_date = agent["death_date"]
        webpage = agent["webpage"]
        new_agent = Agent.query.filter(Agent.name == name).first()
        if not new_agent:
            new_agent = Agent(
                name=name,
                alias=alias,
                birth_date=birth_date,
                death_date=death_date,
                webpage=webpage,
                type=new_type,
            )
            db.session.add(new_agent)
        new_agents.append(new_agent)
    return new_agents


# Function to add new languages to the database
def add_languages(languages):
    new_languages = []
    for language in languages:
        new_language = Language.query.filter(Language.code == language).first()
        if not new_language:
            new_language = Language(code=language)
            db.session.add(new_language)
        new_languages.append(new_language)
    return new_languages


# Function to add new bookshelves to the database
def add_bookshelves(bookshelves):
    new_bookshelves = []
    for bookshelf in bookshelves:
        new_bookshelf = Bookshelf.query.filter(Bookshelf.name == bookshelf).first()
        if not new_bookshelf:
            new_bookshelf = Bookshelf(name=bookshelf)
            db.session.add(new_bookshelf)
        new_bookshelves.append(new_bookshelf)
    return new_bookshelves


# Function to add new subjects to the database
def add_subjects(subjects):
    new_subjects = []
    for subject in subjects:
        new_subject = Subject.query.filter(Subject.name == subject).first()
        if not new_subject:
            new_subject = Subject(name=subject)
            db.session.add(new_subject)
        new_subjects.append(new_subject)
    return new_subjects


# Function to add new publishers to the database
def add_publishers(publishers):
    new_publishers = []
    for publisher in publishers:
        new_publisher = Publisher.query.filter(Publisher.name == publisher).first()
        if not new_publisher:
            new_publisher = Publisher(name=publisher)
            db.session.add(new_publisher)
        new_publishers.append(new_publisher)
    return new_publishers
