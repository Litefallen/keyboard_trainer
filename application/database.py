import sqlite3
import uuid
import click
from flask import current_app, g
# db = sqlite3.connect('userdb.db')
# db.execute("PRAGMA foreign_keys = 1")


# def create_user():
#     db = sqlite3.connect('userdb.db')
#     db.execute("PRAGMA foreign_keys = 1")
    
#     pass
# def user_stats():
#     pass


#table creation
# cursor = db.cursor()
# cursor.execute('''create table users(user_id TEXT PRIMARY KEY, f_name TEXT, surname TEXT, email TEXT)''')
# cursor.execute('''create table user_stats(user_id TEXT, words_per_min REAL DEFAULT 0, accuracy REAL DEFAULT 0, PRIMARY KEY(user_id), foreign key(user_id) references users(user_id) on delete cascade)'''
# )
# cursor.execute('''create table success_per_letter(user_id TEXT,
#                a REAL DEFAULT 0,b REAL DEFAULT 0,c REAL DEFAULT 0,d REAL DEFAULT 0,e REAL DEFAULT 0,f REAL DEFAULT 0,g REAL DEFAULT 0,h REAL DEFAULT 0,i REAL DEFAULT 0,
#                j REAL DEFAULT 0,k REAL DEFAULT 0,l REAL DEFAULT 0,m REAL DEFAULT 0,n REAL DEFAULT 0,o REAL DEFAULT 0,p REAL DEFAULT 0,q REAL DEFAULT 0,r REAL DEFAULT 0,s REAL DEFAULT 0,t REAL DEFAULT 0,u REAL DEFAULT 0,
#                v REAL DEFAULT 0,w REAL DEFAULT 0,x REAL DEFAULT 0,y REAL DEFAULT 0,z REAL DEFAULT 0, PRIMARY KEY(user_id),foreign key(user_id) references users(user_id) on delete cascade)''')
# print(uuid.uuid4())
# cursor.execute('''DROP TABLE user_stats''')
# cur = cursor.execute("insert into users(user_id,f_name) values('red', 'john')")
# db.commit()
# cur.commit()
# cursor.fetchall()
# cursor.execute("select * from users")
# a = cursor.fetchall()
# print(cursor.fetchall())
# cursor.execute("insert into user_stats(user_id,accuracy) values('red',11)")
# cursor.execute("delete from users")
# db.commit()
# cursor.execute("drop table user_stats")
# db.commit()

# cursor.execute("select * from user_stats")
# cursor.execute("select * from users")
# print(cursor.fetchall())
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)