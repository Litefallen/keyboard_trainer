import flask
from flask import Blueprint, redirect, url_for,render_template,request
from .words import json_words_dict, words_taking, rand_test
from .key_listener import randdom_func
from flask_login import login_user, current_user, login_required, logout_user, user_unauthorized
from .database import  add_user,update_user_data,get_user_by_email
from .models import User
from datetime import datetime
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sqla
import webbrowser
# from .database import session




auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login', methods = ['POST', 'GET'])
def login():

    print('login request page')
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = str(request.form['password'])
        try:
            user = get_user_by_email(email)
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
                return redirect(url_for('profile.profile'))
    return render_template('login.html')
    


@auth_bp.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user = get_user_by_email(request.form['email'])
        if user:
            print('error, error')
            flash(message='There already is a user with this email',category='error')
            return render_template('signup.html')
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
            add_user(user)
            login_user(user, remember=True)
            flash(message='The registration was successful!', category='success')
            return redirect(url_for("views.main"))


    return render_template('signup.html')



@auth_bp.route('/logout',methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for("views.main"))

user_profile_bp = Blueprint('profile', __name__)
@user_profile_bp.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    user = get_user_by_email(current_user.email)
    avg_accuracy = [float(i) for i in user.accuracy.split()]
    avg_accuracy = round(sum(avg_accuracy)/len(avg_accuracy),1)
    avg_symbol_p_minute = [float(i) for i in user.symbol_p_minute.split()]
    avg_symbol_p_minute = round(sum(avg_symbol_p_minute)/len(avg_symbol_p_minute),1)
    return render_template('profile.html', user = user, avg_accuracy = avg_accuracy,avg_symbol_p_minute= avg_symbol_p_minute)


@user_profile_bp.route('/update_data', methods = ['GET', 'POST'])
def update_data():
    return update_user_data(current_user)


views = Blueprint('views', __name__)
@views.route('/')
def main():
    # settings to choose
    # amount of words
    # what letter to train
    #theme
    
    return render_template('main_page.html')


@views.route('/typing_test', methods = ["GET", "POST"]) # main page
def typing_test():
    if request.method == 'POST':
        if request.headers['title']=='key_listener':
            key = request.get_json()
            exp_key = key['expected_key']
            key_test = randdom_func
            res = key_test(exp_key)
            return res
        if request.headers['title']=='stats':
            if current_user.is_authenticated:
                stats = request.get_json()
                print(stats)
                user_mail =current_user.email
                return update_user_data(user_mail,stats)
            else:
                print('unauthorized user')
                # flash("Until you're logged in, you are not able to view your statistics",category='error')
                # print(request.url)
                # return webbrowser.open(request.url)
                return redirect(request.url)
        
    if request.method == 'GET':
        params = rand_test()
        print(dict(request.args))
        if 'word_amount_slider' in dict(request.args).keys():
            word_amount = int(dict(request.args)['word_amount_slider'])
            params['string_length'] = word_amount
        if 'desired_letter' in dict(request.args).keys():
            letter = dict(request.args)['desired_letter'].strip('/')
            params['letter'] = letter
        # print('this is the referrer',request.referrer)
        words_list = words_taking(params)
        # words_list = ' '.join(words_list).replace(' ','_')
        words_list = " _ ".join(words_list).split(' ')
        print(words_list, type(words_list))
        # print(words_list)

        return render_template('typing_test.html',words_list= words_list, k_listen_f = randdom_func)
            # return redirect(url_for('views.main'),words_list= words_list, k_listen_f = randdom_func)
    # else:
    #     print('direct request')
    #     words_list = words_taking(rand_test())
    #     words_list = " _ ".join(words_list).split(' ')
    #     # print(words_list)
    #     # words_list = ' '.join(words_list).replace(' ','_')
    #     # print('this is', words_list)
    #     # redirect(url_for('views.typing_test'),words_list= words_list, k_listen_f = randdom_func)
    #     return render_template('typing_test.html',words_list= words_list, k_listen_f = randdom_func)



admin_bp = Blueprint('admin',__name__)
@admin_bp.route('/admin', methods = ['GET', 'POST'])
def admin_panel():
    # return get_user_by_email('jo@gmail.com').email
    print(flask.session.items())
    return request.cookies.get('id')