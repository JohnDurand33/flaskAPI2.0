from flask import render_template 
from app import app

@app.route('/')
def homepage():

    people = ['John', 'Shoha', 'Diane', 'Peyton']

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

@app.route('/test')
def test_page():
    return {
        'test':'testing'
    }

@app.route('/testing2')
def test_page2():
    return {
        'test':'testing'
    }