# ******************* AUTHENTICATION MODULE ****************************** #
# ** Created by Yossep
# ** github: https://github.com/j2B237/
# ** Project : Joblogueur
# ** Description:
#
# Within this module we have many functions designed to help authenticate user
# on his daily blogger work moderator need to be logged in so we provide
# Methods such as :
# register to register a new user
# login to connect an authenticated user
# Ipbannish to bannish Hacking machine ip
# ************************************************************************ #

# Third party import
from flask import (Blueprint, redirect, render_template, url_for, flash, request, abort)
from flask_mail import Message
from flask_login import current_user, login_user

# Local import
from FlaskApp.forms import RegistrationForm, LoginForm, RequestResetForm
from FlaskApp.models import Moderator, Request
from FlaskApp import db, app, bcrypt, mail


# Create a blueprint for the register and auth process
bp = Blueprint('auth', __name__, url_prefix='/auth')


# Send email to the new moderator
def send_mail(moderator):
    msg = Message("Nouvelle inscription moderateur", sender="contact@digitalschools.sn",
                  recipients=["contact@digitalschools.sn"])
    content = "Moderateur : " + str(moderator['username']) + "\n" + " Contact :" + str(moderator['user_mail'])
    msg.body = content
    mail.send(msg)
    return True


# Inscription
@bp.route('/register',methods=['POST', 'GET'])
def register():
    db.create_all()
    form = RegistrationForm()

    if request.method == 'POST':
        username = form.username.data
        user_mail = form.email.data

        # search if user already exist
        user = Moderator.query.filter_by(username=username).first()
        search_mail = Moderator.query.filter_by(email=user_mail).first()

        moderator = {
            "username": username,
            "user_mail": user_mail
        }

        if user:
            flash("Ce nom d'utilisateur existe deja", "danger")
        elif search_mail:
            flash("Cet email existe déja", "danger")
        else:
            send_mail(moderator)

            notification = Request(sender=username, email=user_mail)
            db.session.add(notification)
            db.session.commit()

            flash('Inscription est en cours de validation' , "success")
            return redirect(url_for('auth.register'))

    form.username.data = ""
    form.email.data = ""
    form.password.data = ""

    return render_template("auth/register.html", title='INSCRIPTION', form=form)


# login methods
@bp.route('/login', methods=['POST', 'GET'])
def login():
    db.create_all()

    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.index"))
        else:
            return redirect(url_for("blog.index"))

    form = LoginForm()

    if form.validate_on_submit():
        # Get data from Form
        user_mail = form.email.data
        password = form.password.data

        # search if user already exist
        user = Moderator.query.filter_by(email=user_mail).first()
        checked_password = bcrypt.check_password_hash(user.password, password)

        if user:
            # Check password
            if checked_password:
                login_user(user, remember=False)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin.index'))
            else:
                flash("Mauvais email ou mot de password", "danger")
                return redirect(url_for('auth.login'))
        else:
            flash('Mot de passe ou email incorrect', 'danger')

    return render_template("auth/login.html", title="Connexion", form=form)


# Reset moderator password
@bp.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    db.create_all()
    form = RequestResetForm()

    if form.validate_on_submit():
        flash('Un e-mail a été envoyé avec des instructions pour réinitialiser votre mot de passe', 'info')
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_request.html",title="Réinitialiser le mot de passe",form=form)