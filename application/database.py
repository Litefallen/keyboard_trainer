import sqlite3
import uuid
import click
from flask import current_app, g
import sqlalchemy as sqla
from sqlalchemy.orm import Session
from .models import Base, User


engine = sqla.create_engine('sqlite:///instance/application.sqlite', echo=True)

def get_db():
    # engine = sqlalchemy.create_engine('sqlite:///instance/application.sqlite', echo=True)
    session = Session(engine)
    return session


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('Database inintialized and tables has been createad')

def add_user(user:list):
    session = get_db()
    session.add_all(user)
    session.commit()
    print('the user has been added')

def get_user(email:str):
    session = get_db()
    res = session.scalar(sqla.select(User).where(User.email==email))
    return res
