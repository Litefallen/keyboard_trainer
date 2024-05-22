
import sqlalchemy as sqla
from sqlalchemy.orm import Session
from .models import Base, User

engine = sqla.create_engine('sqlite:///instance/application.sqlite', echo=False)


def session_decorator(func): # will use it as decorator to get rid of necessity of manually closing the db connection
    with Session(engine) as session:
        def session_wrapper(*args):
            return func(*args,session)
    return session_wrapper


def init_db():
    # Base.metadata.drop_all(engine) # clear the database before launch
    Base.metadata.create_all(engine)
    print('Database inintialized and tables has been createad')

@session_decorator
def add_user(user,session):
    session.add(user)
    session.commit()
    print('the user has been added')

@session_decorator
def get_user(id:str,session): # specific function for flask-login
    return session.get(User, id)

@session_decorator # the way an app will get users from db
def get_user_by_email(email:str,session):
    user = session.scalars(sqla.select(User).where(User.email == email)).first()
    return user

@session_decorator
def update_user_data(user_mail,stats,session):
    user = session.scalars(sqla.select(User).where(User.email == user_mail)).first()
    print('This is accuracy',user.accuracy)
    print('This is symbol_p_minute',user.symbol_p_minute)

    if not user.accuracy:
        # print('First test!')
        user.symbol_p_minute = str(stats['symbol_p_minute'])
        user.accuracy = str(stats['accuracy'])
        session.commit()
    else:
        # print('It is not the first test!')
        user.accuracy = user.accuracy + f" {stats['accuracy']}"
        user.symbol_p_minute = user.symbol_p_minute + f" {stats['symbol_p_minute']}"
        session.commit()
    session.commit()
    return 'All done!'