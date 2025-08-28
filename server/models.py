# server/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    posts = db.relationship("Post", backref="author", lazy=True)

    @validates("name")
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Author must have a name.")
        existing_author = Author.query.filter_by(name=value).first()
        if existing_author:
            raise ValueError("Author name must be unique.")
        return value


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

    @validates("title")
    def validate_title(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Post must have a title.")
        return value

    @validates("content")
    def validate_content(self, key, value):
        if len(value.strip()) < 50:
            raise ValueError("Post content must be at least 50 characters long.")
        return value
