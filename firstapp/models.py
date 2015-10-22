from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
 
db = SQLAlchemy()
 
class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(100), unique = True)
  homefolder = db.Column(db.String(100))
  shelltype = db.Column(db.String(120))
  sudopr = db.Column(db.String(120))
  pwdhash = db.Column(db.String(54))
   
  def __init__(self, username, homefolder, shelltype, sudopr, password):
    self.username = username
    self.homefolder = homefolder.lower()
    self.shelltype = shelltype.lower()
    self.sudopr = sudopr.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)