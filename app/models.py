from secrets import token_hex
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import UserMixin
db = SQLAlchemy()

# Data Definition Language (DDL- used for setting up SQL databases) has different rules than Python.

# BEST PRACTICE ########## -> define association tables before class definition for readability and to avoid circular imports / dependencies

followers = db.Table('followers',  # 'followers' is the name of the table
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id'), nullable=False),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('user.id'), nullable=False)
                     )


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    # By assigning PK as true, integer translates to 'Serial'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime,       nullable=False,
                             default=lambda: datetime.now(timezone.utc))
    posts = db.relationship("Post", backref='author')
    token = db.Column(db.String(100), nullable=True)

    # Relationship to manage likes without a dedicated 'Like' table
    # Using 'likes' table as an association table to handle many-to-many relationship
    liked_posts = db.relationship(
        # 'likers' is the name of the relationship in the Post model
        "Post", secondary="likes", lazy='dynamic', back_populates="likers", overlaps="liked_posts")
    followed = db.relationship("User",
                               secondary='followers',
                               lazy='dynamic',
                               # backref='followers',
                               # above is normal way to name backref, but below shows a way to change your backref specifications
                               backref=db.backref('followers', lazy='dynamic'),
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id))

    # DateTime was imported, and translates to "TIMESTAMP" in SQL.  The documentation for datetime will explain how to reference SQL.  The lambda function insures that the datetime is not only pulled once.  By having a function, the program knows to run something every time a new record is created.

    ###### Relationship Tables - IMPORTANT #########
    # posts db.relationship("TableName", backref="name for instance") - Creates an object user(instance).posts that returns all the table data from the Posts table from the user instance based on the user's PK (FK in Posts table is also needed to make this happen.).  Needs to be capitalized when typing PYTHON's reference to the Post (class) table because in Python, classes are capitalized.  Back_populates increase functionality of FK created and is better then backref becasue it future proofs the db in case it becomes more complex.  #For now, use backref and research how back_populates should work#

    # secondary - for join tables - secondary is the name of the Table being joined by the join table.lowercase ('Like" table joins Users and posts.  So put "like")

    # this is necessary in Python for FK relationships.  'posts' will not display as a column, but this will allow us to call all of the data connected to a user thanks to the Post tables FK and the User tables 'posts' relationship that I typed above -> 'user.posts' will pull all of the data associated with said user instance now.

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        # if token expires you would need to put that logic in the login route for flask.  Therre is a tokenization package, RESEARCH!!!!!!!
        self.token = token_hex(16)

    def __repr__(self) -> str:
        return {self.username}

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_created': self.date_created,
            'token': self.token,
            'followed_count': len(self.followers.all()),
            'following_count': len(self.followed.all())
        }


likes = db.Table('likes',  # good when you don't need to reference your joined table directly
                 db.Column('user_id', db.Integer, db.ForeignKey(
                     'user.id'), nullable=False),
                 db.Column('post_id', db.Integer, db.ForeignKey(
                     'post.id'), nullable=False)
                 )  # THIS IS BETTER THAN CREATING A TABLE BECAUSE YOU CREATE RELATIONSHIP COLUMNS THAT ACT LIKE LISTS!  user.liked_posts and posts.in effect.

# IMPORTANT $$$$$ = JOINED tables should be referenced through foreign keys


class Post(db.Model):
    __tablename__ = 'post'
    # By assigning PK as true, integer translates to 'Serial'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.now(timezone.utc))
# Reference the default table name and column using dot notation - 'user id'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    likers = db.relationship(
        "User", secondary="likes", back_populates="liked_posts", overlaps="likers")
    # REMEBER: Foreign Keys need to be thought out -> ERD

    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id   # order of init needs to match order of route data input

    # ensure you add the referenced relationship table name ('likes') as the secondary attribute of class relationship def ('likers') when using a join table

    def like_count(self):
        return len(self.likers)

    def to_dict(self, user=None):
        
        return {
            'id': self.id,
            'title': self.title,
            'img_url': self.img_url,
            'caption': self.caption,
            'date_created': self.date_created.isoformat(),
            'author': self.author.username if self.author else "Unknown",
            'author_id': self.author.id if self.author else None,
            'like_count': self.like_count(),
            'liked': user in self.likers
        }
# class Like(db.Model):
#     __tablename__ = 'like'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)

#     def __init__(self, user_id, post_id):
#         self.user_id = user_id
#         self.post_id = post_id


# class UserSchema(Marshmallow().Schema):
#     class Meta:
#         fields = ['id', 'username', 'password']

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)
