import os

basedir = os.path.abspath(os.path.dirname(__name__)) # looking for absolute path to a file 

class Config():
    FLASK_APP=os.environ.get("FLASK_APP")
    FLASK_DEBUG=os.environ.get("FLASK_DEBUG")
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS=False    #Needed anytime you use SQLALCHEMY Module 