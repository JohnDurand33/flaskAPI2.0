from flask import Flask
from config import Config
from flask_migrate import Migrate
from .models import db


app = Flask(__name__)
app.config.from_object(Config)          # Global variable instantiation to help manage across the application.

db.init_app(app)
migrate = Migrate(app, db)  # Same as this line -> migrate = Migrate(), then on following line: "migrate.init_app(app, db)".  

from . import routes, models