import sqlite3
import uuid
import click
from flask import current_app, g
import sqlalchemy as sqla
from sqlalchemy.orm import Session
from .models import Base, User


engine = sqla.create_engine('sqlite:///instance/application.sqlite', echo=True)

def get_db():
    session = Session(engine)
    return session



def init_db():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('Database inintialized and tables has been createad')

def add_user(user:list):
    session = get_db()
    session.add_all(user)
    session.commit()
    print('the user has been added')

def get_user(field:str,value:str):
    session = get_db()
    print(field, value)
    condition = f"User.{field}=='{str(value)}'"
    user = eval(f'session.scalar(sqla.select(User).where({condition}))')
    return user
def update_data(current_user):
    email = 'nolife0808@gmail.com'
    session = get_db()
    user = get_user('email','nolife0808@gmail.com')
    user.email = 'aafsdasaf'
    session.commit()
    print(user.name)
    # session.scalar(sqla.update(User)).where(User.email == email).values(email = 'askljhfadlkjhfadlkjhadf')
    return 'All done!'