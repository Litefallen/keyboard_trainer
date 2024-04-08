import flask
from flask import Blueprint, redirect, url_for,render_template,request
from .words import json_words_dict, words_taking
from .key_listener import randdom_func
from flask_login import login_user, current_user
from .database import get_db, add_user,get_user
from .models import User
from datetime import datetime
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash



auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login', methods = ['POST', 'GET'])
def login():

    print('login request page')
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = str(request.form['password'])
        try:
            user = get_user(email)
        except AttributeError:
            user = False
            return user 
        if not user:
            flash(message='There is no users with this email',category='error')
        else:
            if not check_password_hash(user.password, password):
                flash(message='Wrong password',category='error')
            else:
                login_user(user)
                # next = flask.request.args.get('next')
                # print('Login was successful!')
                # # if not url_has_allowed_host_and_scheme(next, request.host):
                # #     return flask.abort(400)
                return redirect(url_for('admin.admin_panel'))
    return render_template('login.html')
    


@auth_bp.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        password = str(request.form['password'])
        if password != request.form['retype_password']:
            print('error, error')
            flash(message='Passwords must match',category='error')
            return render_template('signup.html')
        elif len(password) < 6:
            print('error, error')
            flash('Passwords length should be not less than 6 characters',category='error')
            return render_template('signup.html')
        else:
            hshd_pwd = generate_password_hash(password)
            user = User(name = request.form['username'], email = str(request.form['email'].strip()), password = hshd_pwd)
            add_user([user])
            flash(message='The registration was successful!', category='success')
            return redirect(url_for("auth.login"))

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

@views.route('/')
def home():
    # user = UserMixin()
    # user = user.get_id()
    # print(user)
    return 'user'
    


admin_bp = Blueprint('admin',__name__)
@admin_bp.route('/admin', methods = ['GET', 'POST'])
def admin_panel():
    email = 'nolife0808@gmail.com'
    try:
        return current_user
    except AttributeError:
        return 'No user with such email'
