from flask import render_template , request
from app import app
from .forms import SignUpForm

@app.route('/')
def homepage():

    people = ['John', 'Shoha', 'Diane', 'Peyton', 'Mom']

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
    return ('login.html')

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
        else: print('form invalid')

    return render_template('signup.html', form = form)