from flask import render_template , request, redirect, url_for
from app import app
from .forms import SignUpForm
from .models import User, db

@app.route('/')
def homepage():
    people = ['John', 'Shoha', 'Diane', 'Peyton', 'Mom']   #Testing to show what can be done inside of the route function!  Very cool!

    pokemons = [{
        'name':'pikachu',
        'image':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/back/25.png'
    },
                {
        'name':'ditto',
        'image':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/25.png'
    }]

    return render_template('index.html', peeps=people, pokemons=pokemons)


@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup_page():
    form = SignUpForm()
    print(request)
    if request.method == "POST":
        if form.validate():
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