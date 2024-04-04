from flask import Blueprint

ig = Blueprint('ig', __name__, template_folder='ig_templates')

from . import routes