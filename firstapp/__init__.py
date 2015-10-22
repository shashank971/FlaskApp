import os
from flask import Flask
 
app = Flask(__name__)
 
app.secret_key = 'development key'

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'development.db')
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')

from models import db
db.init_app(app)

@app.before_first_request
def init_request():
    db.create_all()
    
import firstapp.routes