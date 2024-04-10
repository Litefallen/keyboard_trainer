import sqlalchemy as sqla
from sqlalchemy.orm import declarative_base
from datetime import datetime
from flask_login import UserMixin
Base = declarative_base()

class User(Base, UserMixin):
    __tablename__= 'users'
    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    name = sqla.Column(sqla.String(100),nullable=False)
    email = sqla.Column(sqla.String, nullable=False, unique=True)
    password = sqla.Column(sqla.String(150), nullable=False)
    date_created = sqla.Column(sqla.String, default=datetime.now().astimezone())
    wpm = sqla.Column(sqla.FLOAT, default=100)
    accuracy = sqla.Column(sqla.FLOAT, default=100)


