# Imports :
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Creating a database
db = SQLAlchemy()

# Initialize the database name as a constant
DBNAME = "database.db"


# Functions :
def create_app():
    """
    function that create the web application
    """
    # Creating the app
    app = Flask(__name__)
    # Adding the secret key
    app.secret_key = "some random text"
    # Connection bewteen the app and the db
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DBNAME}"
    db.init_app(app)
    
    # Importing the differents blueprints
    from .views import views
    from .auth import auth

    # Registering the differents blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")


    # Importing the differents tables
    from .models import Account


    # Creating the database
    create_database(app)

 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.sign_in'
    login_manager.init_app(app)


    @login_manager.user_loader
    def user_load(id):
        return Account.query.get(int(id))


    # Returning the app
    return app


def create_database(app):
    """
    Function that create a database if it doesn't exist already
    :param app: a flask application
    """
    if not path.exists('webapp/' + DBNAME):
        db.create_all(app=app)
        print("Database created")
