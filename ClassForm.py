from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=20)
    ])
    
    email = StringField("Email", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=50),
        validators.Email()
    ])
    
    password = PasswordField("Password", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=25)
    ])
    
    passwordCheck = PasswordField("Confirm Password", validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    
    submit = SubmitField("Register")
       
class LoginForm(FlaskForm):
    email = StringField(
        label="Email",
        validators=[
            validators.DataRequired(),
            validators.Length(min=3, max=50),
            validators.Email()
        ]
    )
    
    password = PasswordField("Password", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=25)
    ])
    
    submit = SubmitField("Login")

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
