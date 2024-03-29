import os

basedir = os.path.abspath(os.path.dirname(__name__)) # looking for absolute path to a file 

class Config():
    FLASK_APP=os.environ.get("FLASK_APP")
    FLASK_DEBUG=os.environ.get("FLASK_DEBUG")