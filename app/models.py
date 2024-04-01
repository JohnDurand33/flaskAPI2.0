from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import UserMixin
db = SQLAlchemy()

# Data Definition Language (DDL- used for setting up SQL databases) has different rules than Python.  

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) # By assigning PK as true, integer translates to 'Serial'
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime,nullable=False, default=lambda: datetime.now(timezone.utc)) 
    # DateTime was imported, and translates to "TIMESTAMP" in SQL.  The documentation for datetime will explain how to reference SQL.  The lambda function insures that the datetime is not only pulled once.  By having a function, the program knows to run something every time a new record is created.
    posts = db.relationship("Post", backref='author') 
    # Needs to be capitalized when typing PYTHON's reference to the Post (class) table because in Python, classes are capitalized.  Back_populates increase functionality of FK created and is better then backref becasue it future proofs the db in case it becomes more complex.  #For now, use backref and research how back_populates should work#

    #this is necessary in Python for FK relationships.  'posts' will not display as a column, but this will allow us to call all of the data connected to a user thanks to the Post tables FK and the User tables 'posts' relationship that I typed above -> 'user.posts' will pull all of the data associated with said user instance now.
    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self.email = email

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True) # By assigning PK as true, integer translates to 'Serial'
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String(500))
    date_created = db.Column(db.DateTime,nullable=False, default=lambda: datetime.now(timezone.utc)) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) # Reference the default table name and column using dot notation -> 'user.id'
    # REMEBER: Foreign Keys need to be thought out -> ERD

