from flask_wtf import FlaskForm
from Web.model import User
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import Length,EqualTo,DataRequired,Email,ValidationError,NumberRange

class LoginForm(FlaskForm):
    email=StringField(label='Email',validators=[Email(),DataRequired()])
    password=PasswordField(label='Password',validators=[Length(min=6),DataRequired()])
    submit=SubmitField(label='Login')
    
class RegisterForm(FlaskForm):
    def validate_email(self, email):
        email1=User.query.filter_by(email=email.data).first()
        if email1:
            raise ValidationError('User with Email already exists!')
        
    name=StringField(label='Name',validators=[Length(min=4,max=20),DataRequired()])
    email=StringField(label='Email',validators=[Email(),DataRequired()])
    password=PasswordField(label='Password',validators=[Length(min=6),DataRequired()])
    password1=PasswordField(label='Confirm Password',validators=[EqualTo('password'),DataRequired()])
    submit=SubmitField(label='Register')

class ItemForm(FlaskForm):
    def validate_name(self, name):
        name1=User.query.filter_by(name=name.data).first()
        if name1:
            raise ValidationError('Item already exists')
    name=StringField(label='Item Name',validators=[Length(min=3),DataRequired()])
    price=IntegerField(label='Price',validators=[NumberRange(min=10),DataRequired()])
    submit=SubmitField(label='Add Item')

class AddForm(FlaskForm):
    submit=SubmitField(label="add")