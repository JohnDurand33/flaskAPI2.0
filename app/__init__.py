from flask import Flask
from config import Config
from flask_migrate import Migrate
from .models import db, User
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)          # Global variable instantiation to help manage across the application.

db.init_app(app)
migrate = Migrate(app, db)  # Same as this line -> migrate = Migrate(), then on following line: "migrate.init_app(app, db)".  

#Login Manager setup
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    # return User.query.filter_by(id=user_id).first()
    return User.query.get(user_id)

from . import routes, models