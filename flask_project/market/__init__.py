# The __init__.py makes this directory a package
# These lines are responsible for starting the flask application

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy # this import converts python classes (Model) into database TABLES--SQLalchemy "gives python app developers the full power and flexibilty of SQL"
from flask_bcrypt import Bcrypt #to encrypt passwords in database 

app = Flask(__name__)   # this magic method let's flask find the local file to start a local web app (it creates a Flask instance)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db' # the key is what flask uses to identify(URI) the value sqlite db file
app.config['SECRET_KEY']='8412ab4692daf739a3483519' # so flask will attack a secure key to the user info from the forms page
db = SQLAlchemy(app) # Object saying; "Hey! am going to create a database with this app using python classes (models) as database table"
# creating an instance of Bcrypt, setting it to a variable to be used throughout the application
bcrypt = Bcrypt(app)
# letting the LoginManager recognize the application
login_manager = LoginManager(app)
login_manager.login_view='login_page' # so login required in routes.py will know which route to lead users to following the Begin! button before they go to the market page
login_manager.login_message_category='info' #so the flashed message will be in a blue color
from market import routes   # so this __init__.py will recognize the routes.py content
