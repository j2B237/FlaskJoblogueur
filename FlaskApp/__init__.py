# ******************* APPLICATION MODULE ****************************** #
# ** Created by Yossep
# ** github: https://github.com/j2B237/
# ** Project : Joblogueur
# ** Description:
#
# This module is the application factory.
# It is intend to configure the app and has only Configuration variables
#
# ************************************************************************ #


# Third party import
from flask import Flask
from flask_mail import Mail
from flask_sitemap import Sitemap
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ipban import IpBan


# create and configure the app
app = Flask(__name__, instance_relative_config=True)

# Check for the security
ip_ban = IpBan(app, ban_count=3, ban_seconds=60)

# load from instance folder config.py file
app.config.from_pyfile('config.py', silent=True)

# Create mail service
mail = Mail(app)

# Encrypt password
bcrypt = Bcrypt()

# DATABASE CONFIG
# engine = create_engine("mysql+pymysql://root:Africa237@@localhost/blogdb")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost/blog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect to Mysql Database
db = SQLAlchemy(app)

# Config for moderator authentication
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message = " Veuillez vous authentifier afin d'accéder à cette page"
login_manager.login_message_category = "info"


# In addition to verify that the user is logged in
login_manager.refresh_view = 'auth.login'
login_manager.needs_refresh_message = "Pour proteger votre compte, veuillez-vous connecter afin d'accéder à cette page"
login_manager.needs_refresh_message_category = "info"

# Create a sitemap for the app
ext = Sitemap(app=app)

# Local import
from . import blog
from . import auth
from . import admin

app.register_blueprint(blog.bp)
app.add_url_rule('/', endpoint='index')

app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
