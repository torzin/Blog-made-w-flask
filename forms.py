from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_ckeditor import CKEditorField
# FORMS


class RegisterForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = EmailField("Your Email", validators=[DataRequired(), Email()])
    password = PasswordField("Your Password", validators=[DataRequired()])
    
    submit = SubmitField("Sign Me Up!")


class CreatePostForm(FlaskForm):
    title = StringField("Your Title ", validators=[DataRequired()])
    content = CKEditorField("Post Content", validators=[DataRequired()])
    description = StringField("Post Description", validators=[DataRequired()])

    submit = SubmitField("Create Post")


class LoginForm(FlaskForm):
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    password = PasswordField("Your Password", validators=[DataRequired()])

    submit = SubmitField("Log In")
