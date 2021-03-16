# ******************* FORMS MODULE ****************************** #
# ** Created by Yossep
# ** github: https://github.com/j2B237/
# ** Project : Digital Schools
# ** Description:
#
# Within this module we have many forms for the website, blog, back office site
# Forms such as :
# Website forms
# ProjectForm
# ContactForm
#
# Authentication form
# RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
#
# Blog Back office
# CategoryForm, PostForm, CommentForm, ModeratorForm, UpdateModeratorForm
#
# Blog Front-office
# NewsletterForm
# ************************************************************************ #


from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField, SubmitField,\
    PasswordField, BooleanField, SelectField, RadioField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import data_required, email, Length, EqualTo, ValidationError
from FlaskApp.models import Moderator


# *********************** ORDER AND CONTACT FORMS ******************** #


class ProjectForm(FlaskForm):
    username = StringField('Votre nom et prénom', validators=[data_required()])
    phone_number = StringField('N° de téléphone', validators=[data_required(), Length(9, 13)])
    email = StringField('Adresse email', validators=[data_required(), email()])
    company = StringField('Ecole ou entreprise')
    website = StringField('Site web')
    hours = DateTimeField('Disponibilité', format='%d-%m-%Y %H:%M:%S')
    project_type = StringField('Votre projet')
    message = TextAreaField('Votre message', validators=[data_required()], description='Faites nous part de vos attentes')
    submit = SubmitField('Contactez-moi')


class ContactForm(FlaskForm):
    username = StringField('Votre nom', validators=[data_required()])
    email = StringField('Adresse Email', validators=[data_required(), email()])
    phone_number = StringField('Portable ou Fixe', validators=[data_required(), Length(9, 14)])
    message = TextAreaField('Votre Message', validators=[data_required()])
    submit = SubmitField('Commander')


# ************** AUTHENTICATION FORMS ****************** #

class RegistrationForm(FlaskForm):
    username = StringField('nom utilisateur',
                           validators=[data_required(), Length(2, 20)])
    email = StringField('Email',
                        validators=[data_required(), email()])
    password = PasswordField('Mot de passe',
                             validators=[data_required(), Length(8, 50)])
    confirm_password = PasswordField('Confirmer mot de passe',
                             validators=[data_required(), Length(8, 50), EqualTo('password')])
    submit = SubmitField("S'inscrire")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[data_required(), email()])
    password = PasswordField('Mot de passe',
                             validators=[data_required(), Length(8, 50)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Connexion')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[data_required(), email()])
    submit = SubmitField('Réinitialiser le mot de passe')

    def validate_email(self, email):
        user = Moderator.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError("Il n'y a pas de compte avec cet e-mail. Vous devez d'abord vous inscrire!")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[data_required()])
    confirm_password = PasswordField('Confirmer mot de passe',
                                     validators=[data_required(), EqualTo('password')])
    submit = SubmitField('Reset mot de passe')


# ******************** BLOG ADMINISTRATION FORMS ************************ #

class CategoryForm(FlaskForm):
    category_name = StringField('Nom de la categorie', validators=[data_required()])
    color = SelectField("Couleur", choices=['primary', 'danger', 'success', 'warning', 'info'])
    submit = SubmitField('Enregistrer et quitter')


class PostForm(FlaskForm):

    title = StringField('Titre', validators=[data_required()])
    introduction = StringField('Introduction', validators=[data_required()])
    p_intro = TextAreaField('Paragraphe introduction', validators=[data_required()])
    img_title = FileField('Upload photo', validators=[FileAllowed(['jpg', 'png', 'webp'])])

    img_h1 = FileField("Upload photo", validators=[FileAllowed(['jpg', 'png', 'webp'])])
    h1 = StringField('Sous-titre 1')
    p_h1 = TextAreaField('Paragraphe sous-titre 1')

    img_h2 = FileField("Upload photo", validators=[FileAllowed(['jpg', 'png', 'webp'])])
    h2 = StringField('Sous-titre 2')
    p_h2 = TextAreaField('Paragraphe sous-titre 2')

    img_h3 = FileField("photo", validators=[FileAllowed(['jpg', 'png','webp'])])
    h3 = StringField('Sous-titre 3')
    p_h3 = TextAreaField('Paragraphe sous-titre 3')

    img_h4 = FileField("Upload photo", validators=[FileAllowed(['jpg', 'png','webp'])])
    h4 = StringField('Sous-titre 4')
    p_h4 = TextAreaField('Paragraphe sous-titre 4')

    img_h5 = FileField("Upload photo", validators=[FileAllowed(['jpg', 'png','webp'])])
    h5 = StringField('Sous-titre 5')
    p_h5 = TextAreaField('Paragraphe sous-titre 5')

    img_h6 = FileField("Upload photo", validators=[FileAllowed(['jpg', 'png','webp'])])
    h6 = StringField('Sous-titre 6')
    p_h6 = TextAreaField('Paragraphe sous-titre 6')

    img_h7 = FileField("Upload photo", validators=[FileAllowed(['jpg', 'png','webp'])])
    h7 = StringField('Sous-titre 7')
    p_h7 = TextAreaField('Paragraphe sous-titre 7')

    img_h8 = FileField("Upload photo", validators=[FileAllowed(['jpg', 'png','webp'])])
    h8 = StringField('Sous-titre 8')
    p_h8 = TextAreaField('Paragraphe sous-titre 8')

    img_h9 = FileField("Upload photo", validators=[FileAllowed(['jpg', 'png','webp'])])
    h9 = StringField('Sous-titre 9')
    p_h9 = TextAreaField('Paragraphe sous-titre 9')

    img_h10 = FileField("Upload photo", validators=[FileAllowed(['jpg', 'png','webp'])])
    h10 = StringField('Sous-titre 10')
    p_h10 = TextAreaField('Paragraphe sous-titre 10')

    conclusion = StringField('Conclusion')
    p_conclusion = TextAreaField('Paragraphe conclusion')

    category = StringField("Categorie", validators=[data_required()])
    Not_Publish = RadioField("Publier Maintenant ?", choices=['Oui','Non'])
    submit = SubmitField('Enregister')


class CommentForm(FlaskForm):
    author = StringField('Nom et Prenom', validators=[data_required(), Length(3, 20)])
    author_email = StringField('Email', validators=[data_required(), email()])
    content = TextAreaField('Commentaire', validators=[data_required()])
    submit = SubmitField('Envoyer')


class ModeratorForm(FlaskForm):
    username = StringField('Nom utilisateur', validators=[data_required(), Length(3, 20)])
    email = StringField('Email utilisateur', validators=[data_required(), email()])
    password = PasswordField('Mot de passe', validators=[data_required(), Length(8, 20)])
    img_file = FileField("Upload photo de profil", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Enregistrer')


class UpdateModeratorForm(FlaskForm):
    username = StringField('Nom utilisateur', validators=[data_required(), Length(3, 20)])
    email = StringField('Email utilisateur', validators=[data_required(), email()])
    password = PasswordField('Mot de passe', validators=[data_required(), Length(8, 20)])
    img_file = FileField("Upload photo de profil", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('valider')