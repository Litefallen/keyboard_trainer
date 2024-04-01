from flask import Blueprint, redirect, url_for,render_template,request
from .words import json_words_dict, words_taking
from .key_listener import randdom_func
# from flask_login import UserMixin
from .database import get_db
from datetime import datetime
from flask import flash, get_flashed_messages
from werkzeug.security import generate_password_hash, check_password_hash



auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login', methods = ['POST', 'GET'])
def login():
    print('login request page')
    if request.method == 'POST':
        import hashlib
        email = request.form['email']
        password = str(request.form['password'])
        # hex_pwd = 'danie@gmail.com'
        
        cursor = get_db().cursor()
        query = "select * from users where email == (?)"
        cursor.execute(query,(email,))
        user_from_db = [column for column in cursor.fetchall()[0]]
        if not user_from_db:
            flash(message='There is no users with this email',category='error')
            return render_template('login.html')
        elif not check_password_hash(user_from_db[2], password):
            flash(message='Wrong password',category='error')
            return render_template('login.html')
        else:
            print('Login was successful')
            return render_template('login.html')
    return render_template('login.html')
    


@auth_bp.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = str(request.form['password'])
        if password != request.form['retype_password']:
            print('error, error')
            flash(message='Passwords must match',category='error')
            return render_template('signup.html')
        elif len(password) < 6:
            print('error, error')
            flash('Passwords length should be not less than 6 characters',category='error')
            return render_template('signup.html')
        # print(type(username), email, type(password))
        # user = UserMixin()
        else:
            cursor = get_db().cursor()
            hshd_pwd = generate_password_hash(password)
            query = "insert into users(username, email, password, date_created) values(?,?,?,?)"
            cursor.execute(query,(username, email, hshd_pwd, datetime.now()))
            get_db().commit()
            return redirect(url_for("auth.login"))

        # print(request.form)
    return render_template('signup.html')
    
    # print(request.method)


@auth_bp.route('/logout')
def logout():
    return redirect(url_for('main'))

user_profile_bp = Blueprint('profile', __name__)
@user_profile_bp.route('/profile')
def profile():
    return 'profile_page'

views = Blueprint('views', __name__)

@views.route('/typing_test') # main page
def main():
    words_list = words_taking('z', 1)
    words_list = ' '.join(words_list).replace(' ','_')
    return render_template('typing_test.html',words_list= words_list, k_listen_f = randdom_func)

@views.route('/fetch_testing/', methods =['post']) # get the expected key, listen for keypress and check the pressed key
def f_testing():
    key = request.get_json()
    exp_key = key['expected_key']
    key_test = randdom_func
    res = key_test(exp_key)
    return res


@views.route('/get_stat_data', methods = ['post'])
def get_stat_data():
    data = request.get_json()
    print(data)
    # data['speed'] = data['end'] - data['start']
    # data['speed'] = str(datetime.fromisoformat(data['end']) - datetime.fromisoformat(data['start']))
    # print(data['speed'])
    return data
    # add data to database