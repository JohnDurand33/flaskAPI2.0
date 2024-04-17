from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import UserMixin
db = SQLAlchemy()
from werkzeug.security import generate_password_hash

# Data Definition Language (DDL- used for setting up SQL databases) has different rules than Python.  
followers = db.Table('followers',
                    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), nullable= False),
                    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), nullable= False)
                    )   
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) # By assigning PK as true, integer translates to 'Serial'
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime,nullable=False, default=lambda: datetime.now(timezone.utc))
    posts = db.relationship("Post", backref='author') 
    # liked_posts = db.relationship("Post", secondary="like")  # below line is how to manage likes without a Like table
    liked_post2 = db.relationship("Post", secondary="like2", lazy='dynamic') # gives a list of posts from current_user.  When user likes a post, they provide  apost id, which can be used as the query variable for the Post table, and then append it to the liked_posts column.  The system automatically commits to this table so your commit isn't needed
    followed = db.relationship("User", 
                                secondary='followers', 
                                lazy='dynamic',
                                # backref='followers',  
                                # above is normal way to name backref, but below shows a way to change your backref specifications
                                backref=db.backref('followers', lazy='dynamic'),
                                primaryjoin= (followers.c.follower_id == id),
                                secondaryjoin= (followers.c.followed_id == id))
    

    # DateTime was imported, and translates to "TIMESTAMP" in SQL.  The documentation for datetime will explain how to reference SQL.  The lambda function insures that the datetime is not only pulled once.  By having a function, the program knows to run something every time a new record is created.

    ###### - IMPORTANT #########
    # posts dn.relationship("TableName", backref="name for instance") - Creates an object user(instance).posts that returns all the table data from the Posts table from the user instance based on the user's PK (FK in Posts table is also needed to make this happen.).  Needs to be capitalized when typing PYTHON's reference to the Post (class) table because in Python, classes are capitalized.  Back_populates increase functionality of FK created and is better then backref becasue it future proofs the db in case it becomes more complex.  #For now, use backref and research how back_populates should work#

    #secondary - for join tables - secondary is the name of the Table being joined by the join table.lowercase ('Like" table joins Users and posts.  So put "like") 

    #this is necessary in Python for FK relationships.  'posts' will not display as a column, but this will allow us to call all of the data connected to a user thanks to the Post tables FK and the User tables 'posts' relationship that I typed above -> 'user.posts' will pull all of the data associated with said user instance now.
    def __init__(self, username, email, password):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True) # By assigning PK as true, integer translates to 'Serial'
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String(500))
    date_created = db.Column(db.DateTime,nullable=False, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) # Reference the default table name and column using dot notation - 'user id'
    # likers = db.relationship("User", secondary="like")
    likers2 = db.relationship("User", secondary="like2") # added 2 to secondary when using variable table below like_count function below
    # REMEBER: Foreign Keys need to be thought out -> ERD

    def __init__(self, title, caption, img_url, user_id):
        self.title = title
        self.caption = caption
        self.img_url = img_url
        self.user_id = user_id   # order of init needs to match order of route data input

    def like_count(self):
        return len(self.likers2)
    
    def to_dict(self, user=None):
        return {
            'id': self.id,
            'title': self.title,
            'img_url': self.img_url,
            'caption': self.caption,
            'date_created': self.date_created,
            'user_id': self.user_id,
            'author': self.author.username,
            'like_count': self.like_count(),
            # 'liked': user in self.likers2
            'liked':False
        }

like2 = db.Table('like2',  # good when you don't need to reference your joined table directly
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable = False),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable = False)
                ) #THIS IS BETTER THAN CREATING A TABLE BECAUSE YOU CREATE RELATIONSHIP COLUMNS THAT ACT LIKE LISTS!  user.liked_posts2 and posts.in effect.

# class Like(db.Model):
#     __tablename__ = 'like'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False) 

#     def __init__(self, user_id, post_id):
#         self.user_id = user_id
#         self.post_id = post_id


##### IMPORTANT $$$$$ = joined tables that never have to be referenced directly (by their id).  joined tables should be referenced through foreign keys







