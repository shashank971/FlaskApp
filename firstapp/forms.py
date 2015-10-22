from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField,validators, ValidationError, PasswordField, SelectField, RadioField
from wtforms.validators import Required, Email
from models import db, User

# class ContactForm(Form):
#   name = TextField("Name", validators=[Required("Please enter your name.")])
#   email = TextField("Email", validators=[Required("Please enter your email."), Email("Please enter your email in right format.")])
#   subject = TextField("Subject", validators=[Required("Please enter your subject.")])
#   message = TextAreaField("Message", validators=[Required("Please enter your message.")])
#   submit = SubmitField("Send")

class SignupForm(Form):
  username = TextField("User name",  validators=[Required("Please enter your user name.")])
  homefolder = TextField("Home folder",  validators=[Required("Please enter your home folder name.")])
  shelltype = SelectField('Shell type', choices=[('bash','Bash'),('b','b shell'), ('csh', 'csh'), ('ksh','ksh'),('tcsh','tcsh'),('zsh','zsh')], validators=[Required("Select your shell type")])
  password = PasswordField('Password', validators=[Required("Please enter a password.")])
  sudopr = SelectField('Sudo privileges', choices=[('yes','Yes'),('no','No')],validators=[Required("Mention if you need sudo privileges?")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(username = self.username.data.lower()).first()
    if user:
      self.username.errors.append("That username is already taken")
      return False
    else:
      return True

class SigninForm(Form):
  username = TextField("Username",  validators=[Required("Please enter your username.")])
  password = PasswordField('Password', validators=[Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(username = self.username.data).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.username.errors.append("Invalid username or password")
      return False

class DeleteForm(Form):
	submit = SubmitField("Delete User")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

class ModifyForm(Form):
	#username = TextField("User name",  validators=[Required("Please enter your user name.")])
  	homefolder = TextField("Home folder",  validators=[Required("Please enter your home folder name.")])
  	shelltype = SelectField('Shell type', choices=[('bash','Bash'),('b','b shell'), ('csh', 'csh'), ('ksh','ksh'),('tcsh','tcsh'),('zsh','zsh')], validators=[Required("Select your shell type")])
  	sudopr = SelectField('Sudo privileges', choices=[('yes','Yes'),('no','No')],validators=[Required("Mention if you need sudo privileges?")])
	submit = SubmitField("Modify User")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
