from flask import Flask
from .config import Config
from flask_migrate import Migrate
from .models import db as root_db
from . import routes, models

app = Flask(__name__)
app.config.from_object(Config)          # Global variable instantiation to help manage across the application.

root_db.init_app(app)
migrate = Migrate(app, root_db, compare_type=True)  # Same as this line -> migrate = Migrate(), then on following line: "migrate.init_app(app, db)".  

