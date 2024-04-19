from flask import Flask
from config import Config
from flask_migrate import Migrate
from .models import db, User
from flask_login import LoginManager
from flask_moment import Moment
from flask_cors import CORS
from .api import api
from .ig import ig

app = Flask(__name__)

# Global variable instantiation to help manage across the application.
app.config.from_object(Config)

CORS(app, resources={r"/api/*": {
    "origins": "*",
    "allow_headers": ["Content-Type", "Authorization"],
    "methods": ["OPTIONS", "POST", "GET"]
}})

app.register_blueprint(ig)
app.register_blueprint(api, url_prefix='/api')

db.init_app(app)

migrate = Migrate(app, db)  # Same as this line -> migrate = Migrate(), then on following line: "migrate.init_app(app, db)".  
#Login Manager setup
login_manager = LoginManager(app)
moment = Moment(app)

@login_manager.user_loader
def load_user(user_id):
    # return User.query.filter_by(id=user_id).first()
    return User.query.get(user_id)

login_manager.login_view = 'login_page' # with the @login_required decorator, this will redirect to the login page if the user is not logged in.  Keeps users from accessing pages they shouldn't be able to access by typing in the address manually.

from . import routes, models