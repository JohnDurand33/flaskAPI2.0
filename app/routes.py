from flask import render_template , request, redirect, url_for, session, flash, get_flashed_messages, abort
from app import app
from .forms import SignUpForm, LogInForm
from .models import User, db, like2
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from werkzeug.security import check_password_hash

############ AUTH ############

@app.route('/login', methods=['GET', 'POST'])  # note:  Can have more than one route decorator for a single function.  This is useful for when you want to have multiple URLs that point to the same page.
def login_page():
    form = LogInForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            # find user in db
            user = User.query.filter_by(username=username).first()
            print(user.password, password)

            if user:
                print(user.username, user.password, user.email)
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash('Logged in successfully', 'success')
                    return redirect(url_for('ig.homepage'))
                else:
                    flash('incorrect username/password', 'danger')

            else:
                flash('That username\password doesn\'t exist.', 'danger')

        else:
            flash('form invalid', 'danger')


    return render_template('login.html', form=form)

# @app.route('/signup', methods=['GET','POST'])
# def signup_page():
#     form = SignUpForm()
#     print(request)
#     if request.method == "POST":
#         if form.validate_on_submit():
#             username = form.username.data
#             email = form.email.data
#             password = form.password.data
            
#             # Add user to database
#             user = User(username, email, password)
#             print(user.username, user.password, password)
#             # user.username = username
#             # user.email = email
#             # user.password = password   # NOT NEEDED WITH __init__ added for class User.  Now just add vars to User parameters instead of leaving User() empty.

#             db.session.add(user)
#             db.session.commit()
#             flash('User created successfully', 'success')

#             return redirect(url_for('login_page'))

#         flash('form invalid', 'danger')

#     return render_template('signup.html', form = form)


@app.route('/logout')
def lougout():
    logout_user()
    return redirect(url_for('ig.homepage'))