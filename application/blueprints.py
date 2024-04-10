import flask
from flask import Blueprint, redirect, url_for,render_template,request
from .words import json_words_dict, words_taking
from .key_listener import randdom_func
from flask_login import login_user, current_user, login_required, logout_user
from .database import get_db, add_user,get_user,update_data
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
            user = get_user('email',email)
        except AttributeError:
            user = False
            return user 
        if not user:
            flash(message='There is no users with this email',category='error')
        else:
            if not check_password_hash(user.password, password):
                flash(message='Wrong password',category='error')
            else:
                login_user(user, remember=True)
                return redirect(url_for('views.something'))
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



@auth_bp.route('/logout',methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

user_profile_bp = Blueprint('profile', __name__)
@user_profile_bp.route('/profile')
@login_required
def profile():
    return 'profile_page'

views = Blueprint('views', __name__)

@views.route('/typing_test', methods = ["GET", "POST"]) # main page
def main():
    if request.method == 'POST':
        if request.headers['title']=='key_listener':
            key = request.get_json()
            exp_key = key['expected_key']
            key_test = randdom_func
            res = key_test(exp_key)
            return res
        if request.headers['title']=='stats':
            stats = request.get_json()
            return stats

    else:
        words_list = words_taking('z', 1)
        words_list = ' '.join(words_list).replace(' ','_')
        return render_template('typing_test.html',words_list= words_list, k_listen_f = randdom_func)


admin_bp = Blueprint('admin',__name__)
@admin_bp.route('/admin', methods = ['GET', 'POST'])
def admin_panel():
    update_data('nolife0808@gmail.com')
    return '1'