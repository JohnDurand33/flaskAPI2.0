from flask import render_template , request, redirect, url_for, session
from app import app
from .forms import SignUpForm, LogInForm, PostForm
from .models import User, Post, db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask import abort

# LOGIN

@app.route('/login', methods=['GET', 'POST'])  # note:  Can have more than one route decorator for a single function.  This is useful for when you want to have multiple URLs that point to the same page.
def login_page():
    form = LogInForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            # find user in db

            user = User.query.filter_by(username=username).first()

            if user:
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('homepage'))
                else:
                    print('incorrect password')

            else:
                print('That username doesn\'t exist.')

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup_page():
    form = SignUpForm()
    print(request)
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            print(f'username {username} | email | {email}, password | {password}')
            
            # Add user to database
            user = User(username, email, password)
            # user.username = username
            # user.email = email
            # user.password = password   # NOT NEEDED WITH __init__ added for class User.  Now just add vars to User parameters instead of leaving User() empty.

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login_page'))

        else: print('form invalid')

    return render_template('signup.html', form = form)


@app.route('/logout')
def lougout():
    logout_user()
    return redirect(url_for('homepage'))

# ROUTES

@app.route('/')
@app.route('/posts')
def homepage():

    posts = Post.query.all()
    if posts:
        return render_template('index.html', posts=posts)

    # people = ['John', 'Shoha', 'Diane', 'Peyton', 'Mom']   #Testing to show what can be done inside of the route function!  Very cool!
    
    else:
        return redirect(url_for('home_page'))
    

    # pokemons = [{
    #     'name':'pikachu',
    #     'image':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/back/25.png'
    # },
    #             {
    #     'name':'ditto',
    #     'image':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/25.png'
    # }]

    # return render_template('index.html', peeps=people, pokemons=pokemons)


@app.route('/posts/<post_id>')
def single_post_page(post_id):
    # post = Post.query.filter_by(id=post_id).first() 
    post = Post.query.get(post_id)  # this and above line are identicle.  .get should be used for PRIMARY KEYS ONLY

    if post == None:
        abort(404)

    if current_user.id == post.user_id:
        return render_template('singlepost.html', post=post)
    else:
        return redirect(url_for('homepage'))

@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post_page():
    form = PostForm()
    if request.method == 'POST':
        if form.validate():

            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data

            my_post = Post(title, caption, img_url, current_user.id)

            db.session.add(my_post)
            db.session.commit()

            return redirect(url_for('homepage'))

    return render_template('createpost.html', form=form)

@app.route('/posts/update/<post_id>', methods=['GET', 'POST'])
@login_required
def update_post_page(post_id):

    post = Post.query.get(post_id) #OR Post.query.filter_by(post_id=post_id).first()
    if current_user.id != post.user_id:
        return redirect(url_for('homepage'))
    form=PostForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data

            post.title = title
            post.caption = caption
            post.img_url = img_url

            db.session.commit()
            return redirect(url_for('single_post_page', post_id=post.id))

    return render_template('updatepost.html', post=post, form=form)

@app.route('/posts/delete/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):

    post = Post.query.get(post_id) #OR Post.query.filter_by(post_id=post_id).first()
    if current_user.id != post.user_id:
        return redirect(url_for('homepage'))
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('homepage'))