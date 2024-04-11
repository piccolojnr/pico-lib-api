from app import db
from sqlalchemy.ext.hybrid import hybrid_property
import enum


class AgentType(enum.Enum):
    ANNOTATOR = "annotator"
    AUTHOR = "author"
    COMMENTATOR = "commentator"
    COMPILER = "compiler"
    COMPOSER = "composer"
    CONTRIBUTOR = "contributor"
    EDITOR = "editor"
    ILLUSTRATOR = "illustrator"
    OTHER = "other"
    PHOTOGRAPHER = "photographer"
    TRANSLATOR = "translator"


book_agents_association = db.Table(
    "book_agents",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column("agent_id", db.Integer, db.ForeignKey("agents.id", ondelete="CASCADE")),
    db.PrimaryKeyConstraint("book_id", "agent_id"),
)


class Agent(db.Model):
    """ """

    __tablename__ = "agents"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    alias = db.Column(db.String)
    birth_date = db.Column(db.String)
    death_date = db.Column(db.String)
    webpage = db.Column(db.String)
    type = db.Column(db.Enum(AgentType), default=AgentType.OTHER, nullable=False)

    books = db.relationship(
        "Book", secondary=book_agents_association, back_populates="agents"
    )

    @hybrid_property
    def agent_books(self):
        from app.models.books import Book

        return Book.query.filter(Book.agents.any(Agent.id == self.id)).limit(5).all()

    @hybrid_property
    def agent_type(self):
        return self.type.value

    def __repr__(self):
        return f"<Agent {self.name}>"
