import sqlite3


db = sqlite3.connect("/home/litefallen/Documents/Python/keyboard_trainer/instance/application.sqlite")
cursor = db.cursor()
# cursor.execute("select * from users")
# cursor.execute(f"insert into users(username, email, password, date_created) values('sa', 'ss33ss', '1111', '22')")
# db.commit()
cursor.execute("select * from users")
print(cursor.fetchall())