# ******************* MODELS MODULE ****************************** #
# ** Created by Yossep
# ** github: https://github.com/j2B237/
# ** Project : Digital Schools
# ** Description:
#
# This module include declarations of all used models
# Models such as :
# Post, Category, Comment, Moderator, Request
#
#
# ************************************************************************ #


from datetime import datetime
from FlaskApp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Moderator.query.get(int(user_id))


# Create all tables
def init_db():
    db.create_all()


class Moderator(db.Model, UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, default='admin1234')
    address1 = db.Column(db.String(20), unique=False, nullable=False, default='address 1')
    address2 = db.Column(db.String(20), unique=False, nullable=False, default='address 2')
    city = db.Column(db.String(20), unique=False, nullable=False, default='your town')
    state = db.Column(db.String(20), unique=False, nullable=False, default='state')
    country = db.Column(db.String(20), unique=False, nullable=False, default='country')
    zipcode = db.Column(db.String(20), unique=False, nullable=False, default='zipcode')
    is_admin = db.Column(db.BOOLEAN, nullable=False, default=False)
    img_file = db.Column(db.String(100), nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    posts = db.relationship("Post", backref="moderator", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return "< Moderator: username: {} | email: {} |address1: {} >".format(self.username, self.email, self.address1)


class Post(db.Model):

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    img_title = db.Column(db.String(80), nullable=True)

    introduction = db.Column(db.String(300), nullable=False, unique=True)
    p_intro = db.Column(db.Text, nullable=False)
    # Sub_title_1 and paragraph
    img_h1 = db.Column(db.String(80), nullable=True)
    h1 = db.Column(db.String(200), nullable=True)
    p_h1 = db.Column(db.Text, nullable=True)

    # Sub_title_2 and paragraph
    img_h2 = db.Column(db.String(80), nullable=True)
    h2 = db.Column(db.String(200), nullable=True)
    p_h2 = db.Column(db.Text, nullable=True)

    # Sub_title_3 and paragraph
    img_h3 = db.Column(db.String(80), nullable=True)
    h3 = db.Column(db.String(200), nullable=True)
    p_h3 = db.Column(db.Text, nullable=True)

    # Sub_title_4 and paragraph
    img_h4 = db.Column(db.String(80), nullable=True)
    h4 = db.Column(db.String(200), nullable=True)
    p_h4 = db.Column(db.Text, nullable=True)

    # Sub_title_5 and paragraph
    img_h5 = db.Column(db.String(80), nullable=True)
    h5 = db.Column(db.String(200), nullable=True)
    p_h5 = db.Column(db.Text, nullable=True)

    # Sub_title_6 and paragraph
    img_h6 = db.Column(db.String(80), nullable=True)
    h6 = db.Column(db.String(200), nullable=True)
    p_h6 = db.Column(db.Text, nullable=True)

    # Sub_title_7 and paragraph
    img_h7 = db.Column(db.String(80), nullable=True)
    h7 = db.Column(db.String(200), nullable=True)
    p_h7 = db.Column(db.Text, nullable=True)

    # Sub_title_8 and paragraph
    img_h8 = db.Column(db.String(80), nullable=True)
    h8 = db.Column(db.String(200), nullable=True)
    p_h8 = db.Column(db.Text, nullable=True)

    # Sub_title_9 and paragraph
    img_h9 = db.Column(db.String(80), nullable=True)
    h9 = db.Column(db.String(200), nullable=True)
    p_h9 = db.Column(db.Text, nullable=True)

    # Sub_title_10 and paragraph
    img_h10 = db.Column(db.String(80), nullable=True)
    h10 = db.Column(db.String(200), nullable=True)
    p_h10 = db.Column(db.Text, nullable=True)
    # Conclusion
    conclusion = db.Column(db.String(200), nullable=True, default='Conclusion')
    p_conclusion = db.Column(db.Text, nullable=True)

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    display_or_not = db.Column(db.BOOLEAN, nullable=False, default=False)
    moderator_id = db.Column(db.Integer, db.ForeignKey("moderator.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return "< Post : {} - {} - Author_id :{}".format(self.title, self.introduction, self.moderator_id)


class Comment(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name_author = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(50), nullable=False, default='default.jpg')
    email_author = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    approved_or_not = db.Column(db.BOOLEAN, nullable=False, default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    @property
    def approved_comment_status(self):
        if not self.approved_or_not:
            self.approved_or_not = True

        return self.approved_or_not

    def __repr__(self):
        return "<Comment - author:{}, email:{} , approved_or_not:{} >".format(self.name_author, self.email_author, self.approved_or_not)


class Category(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    color = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    posts = db.relationship("Post", backref="category", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return "< Category : name= {} | color={} >".format(self.category_name, self.color)


class Request(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    sender = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    validate_or_not = db.Column(db.BOOLEAN, nullable=False, default=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return "< Request: n° {} - {} | {} >".format(self.id, self.sender, self.email)
