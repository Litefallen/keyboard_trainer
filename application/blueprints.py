
from flask import Blueprint, redirect, url_for,render_template,request
from .words import words_taking, rand_test
from .key_listener import k_listener
from flask_login import login_user, current_user, login_required, logout_user, user_unauthorized
from .database import  add_user,update_user_data,get_user_by_email
from .models import User
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash






auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login', methods = ['POST', 'GET'])
def login(): # get email from request, try to get the user from db, if user exists - redirect to profile page, if not - flash notification. Check for correct password as well.
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
def signup(): # user registration
    if request.method == 'POST':
        user = get_user_by_email(request.form['email']) # try to get the user from db
        if user: 
            print('error, error')
            flash(message='There already is a user with this email',category='error')
            return render_template('signup.html')
        password = str(request.form['password']) # get the entered password and check it
        if password != request.form['retype_password']:
            print('error, error')
            flash(message='Passwords must match',category='error')
            return render_template('signup.html')
        elif len(password) < 6:
            print('error, error')
            flash('Passwords length should be not less than 6 characters',category='error')
            return render_template('signup.html')
        else: # if its a new user - create password hash, store the new user in db and login it
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

user_profile_bp = Blueprint('profile', __name__) # profile page with stats
@user_profile_bp.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    user = get_user_by_email(current_user.email)
    if user.accuracy:
        avg_accuracy = [float(i) for i in user.accuracy.split()]
        avg_accuracy = round(sum(avg_accuracy)/len(avg_accuracy),1)
    else:
        avg_accuracy = 0
    if user.symbol_p_minute :
        avg_symbol_p_minute = [float(i) for i in user.symbol_p_minute.split()]
        avg_symbol_p_minute = round(sum(avg_symbol_p_minute)/len(avg_symbol_p_minute),1)
    else:
        avg_symbol_p_minute = 0
    return render_template('profile.html', user = user, avg_accuracy = avg_accuracy,avg_symbol_p_minute= avg_symbol_p_minute)


@user_profile_bp.route('/update_data', methods = ['GET', 'POST'])
def update_data():
    return update_user_data(current_user)


views = Blueprint('views', __name__) # main page
@views.route('/')
def main():
    print(request.server)
    print(request.root_path)
    return render_template('main_page.html')


@views.route('/typing_test', methods = ["GET", "POST"]) # typing practice
def typing_test():
    if request.method == 'POST': 
        if request.headers['title']=='key_listener':# code for key listener
            key = request.get_json() # get the expected key, run the fuction to listen user keyboard and waiting for key press
            exp_key = key['expected_key']
            if exp_key == '_':
                exp_key = 'space'
            key_test = k_listener()
            print('expected key is:', exp_key)
            print('the pressed key is:', key_test)
            res = {'result': True} if exp_key ==key_test else {'result':False}
            if key_test == 'esc':
                res['result'] = 'Abort'
            return res

        if request.headers['title']=='stats': # get the typing stats after typing practice finish
            if current_user.is_authenticated: # if user is authorized - save stats to db
                stats = request.get_json()
                print('this is stats', stats)
                user_mail =current_user.email
                return update_user_data(user_mail,stats)
            else:
                print('unauthorized user')
        
    if request.method == 'GET':
        params = rand_test() # create defult settings for typing practice
        if 'letter' in request.args: # replace default settings if specific settings are provided
            params['letter'] = dict(request.args)['letter'].strip('/')
        if 'string_length' in request.args:
            params['string_length'] = int(dict(request.args)['string_length'])
        words_list = words_taking(params) 
        words_list = " _ ".join(words_list).split(' ')
        # generate the string with selected words, divided by '_' to represent space key.
        return render_template('typing_test.html',words_list= words_list, k_listen_f = k_listener, test_settings = params)
