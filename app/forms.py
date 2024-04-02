from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email

class SignUpForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm your password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LogInForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField()

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    caption = StringField("Caption")
    submit = SubmitField()
