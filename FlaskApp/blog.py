# ******************* BLOG MODULE ****************************** #
# ** Created by Yossep
# ** github: https://github.com/j2B237/
# ** Project : Joblogueur
# ** Description:
#
# Within this module we have many functions designed to help display posts
# Methods such as :
# display all posts
# display posts per category
# display individual post
# register email user for the newsletter
# ************************************************************************ #

# Third party import
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_mail import Message

# Local import
from FlaskApp.models import Post, Category, Moderator, Comment
from FlaskApp.forms import CommentForm
from . import db, ext, mail


bp = Blueprint('blog', __name__)

# Fake data to seed the website view
fake_Category = [
                    {
                        'id': 1,
                        'category_name': "10 bonnes raisons",
                        'color': 'primary'
                    },
                    {
                        'id': 2,
                        'category_name':  "Comment réussir ?",
                        'color': 'success',
                    },
                    {
                        'id': 3,
                        'category_name': "Offres et formations",
                        'color': 'warning'
                    }
                ]

fake_moderators = [
                    { 'id': 1,
                      'username': 'admin',
                      'email': 'admin@exemple.com',
                      'password': 'admin237',
                      'address1': 'address1',
                      'address2': 'address2',
                      'city': 'city',
                      'state': 'state',
                      'country': 'country',
                      'zipcode': 'zipcode',
                      'is_admin': True,
                      'image_file': 'default.jpg',
                      'created_on': '21/02/2021',
                      'posts': []
                      }
                    ]

fake_posts = [
                {
                    'id': 1,
                    'title': 'Comment réussir à gagner de l\'argent sur internet',
                    'introduction': 'Qu\’ils soient aujourd\’hui milliardaires ou non, reconnus à l\’international ou en France.',
                    'p_intro': 'Ils ont tous commencer simplement. Pour toi modeste citoyen qui voudrait gagner de l\'argent pour arrondir tes fins du mois, nous avons sélectionner une liste de sites et bonnes astuces à essayer',
                    'h1': "",
                    'p_h1': "",
                    'h2': "",
                    'p_h2': "",
                    'h3': "",
                    'p_h3': "",
                    'h4': "",
                    'p_h4': "",
                    'h5': "",
                    'p_h5': "",
                    'conclusion': "",
                    'p_conclusion': "",
                    'date_posted': '10/02/2021',
                    'display_or_not': True,
                    'moderator_id': 1,
                    'category_id': 1,
                    'comments': [],
                }
                ]

fake_comments = [
                    {
                        'id': 1,
                        'author_name': 'admin',
                        'email_author': 'admin@exemple.com',
                        'content': 'C\'est bon tout ca.',
                        'date_posted': '12/02/2021',
                        'approved_or_not': True,
                        'post_id': 1
                    }
                ]

# Create a sitemap
@ext.register_generator
def index():
    yield 'index', {}

# Home blog view
@bp.route('/')
def index():
    global fake_moderators, fake_comments, fake_posts, fake_Category

    categories = Category.query.all()
    moderators = Moderator.query.all()

    posts_to_display = Post.query.all()

    post_banner = Post.query.join(Category).filter(Category.category_name == "BUSINESS").\
        order_by(Post.date_posted.desc()).first()

    last_post = Post.query.join(Category).filter(Category.category_name == "TUTORIELS").order_by(
        Post.date_posted.desc()).first()

    posts_for_cards = Post.query.filter_by(display_or_not=True).order_by(Post.date_posted.desc())[:4]

    post_business = Post.query.join(Category).filter(Category.category_name == "BUSINESS").\
        order_by(Post.date_posted.desc()).first()
    post_formation = Post.query.join(Category).filter(Category.category_name == "FORMATIONS"). \
        order_by(Post.date_posted.desc()).first()

    post_tutoriel = Post.query.join(Category).filter(Category.category_name == "TUTORIELS"). \
        order_by(Post.date_posted.desc()).first()

    post_ressource = Post.query.join(Category).filter(Category.category_name == "RESSOURCES"). \
        order_by(Post.date_posted.desc()).first()

    image_posts = []
    for post in posts_for_cards:
        image = post.img_title
        image_posts.append(image)

    return render_template('blog/blog.html', title="Accueil - Joblogueur",
                           categories=categories, last_post=last_post,moderators=moderators,
                           images=image_posts, posts_to_display=posts_to_display,
                           post_banner=post_banner, post_business=post_business,
                           post_formation=post_formation, post_tutoriel=post_tutoriel, post_ressource=post_ressource)


# Display individual post
@bp.route('/publication/<post_title>', methods=['POST', 'GET'])
def post(post_title):

    form = CommentForm()
    titre = post_title.replace('-', ' ')
    # Recherche la publication par son titre
    post = Post.query.filter_by(title=titre).first()
    moderators = Moderator.query.all()

    # Recherche tous les commentaires liés à cette publication
    comments_to_display = Comment.query.join(Post).filter(Comment.post_id == post.id).\
        order_by(Comment.date_posted.desc()).all()

    # Liste toutes les categories
    categories = Category.query.all()
    nbr_comments = 0

    # Calcul le nbre de commentaires par publication
    for comment in post.comments:
        if comment.approved_or_not:
            nbr_comments += 1

    if form.validate_on_submit():
        search_comments = Comment.query.filter_by(email_author=form.author_email.data).all()
        ids = []
        for comment in search_comments:
            ids.append(comment.post_id)

        if post.id in ids:
            flash("Vous avez deja commenté cet article", "info")

        # Création d'un commentaire
        else:
            new_comment = Comment(name_author=form.author.data, email_author=form.author_email.data,
                                  content=form.content.data, post_id=post.id, approved_or_not=False)
            db.session.add(new_comment)
            db.session.commit()

            form.author.data = ""
            form.author_email.data = ""
            form.content.data = ""
            flash("Votre commentaire est en cours de validation", "success")
            return render_template('blog/blog_post.html', title=titre + " | Joblogueur", post=post, form=form,
                                   nbr_comments=int(nbr_comments), categories=categories, comments=comments_to_display,
                                   titre=post_title)
    form.author.data = ""
    form.author_email.data = ""
    form.content.data = ""

    image_file = url_for('static', filename='upload/'+str(post.img_title))
    return render_template("blog/blog_post.html", title=titre + " | Joblogueur", post=post, form=form,
                           nbr_comments=int(nbr_comments), categories=categories,
                           comments=comments_to_display, image=image_file, moderators=moderators,
                           titre=post_title)


# Display post per category
@bp.route('/publications/<category_name>')
def post_per_category(category_name):

    page = request.args.get('page', 1, type=int)
    search_category = category_name.replace('-', ' ')
    categories = Category.query.all()
    posts = Post.query.join(Category).filter(Category.category_name == search_category).\
        order_by(Post.date_posted.desc()).paginate(per_page=7, page=page)

    image_posts = []
    for post in posts.items:
        image = post.img_title
        image_posts.append(image)

    return render_template("blog/posts_per_category.html", title=search_category + " | Joblogueur", posts=posts,
                           categories=categories, search_category=search_category, images=image_posts)


# Register user for daily news
@bp.route('/newsletter-invitation', methods=['POST','GET'])
def newsletter_invitation():

    categories = Category.query.all()
    posts_per_category = []

    for category in categories:
        last_post = Post.query.join(Category).filter(Post.category_id == category.id).first()
        posts_per_category.append(last_post)

    if request.method == 'POST':
        usermail = request.form['usermail']
        content = """
            Salut très cher(e),

            Comment vas-tu ?
            
            Il y'a du nouveau sur ton blog préféré www.digitalschools.sn/blog
            
            Ci-dessous une liste des publications que tu as surement manqués:
            
            1- https://3df5e7df0cdb.ngrok.io/blog/publication/10-raisons-pourquoi-toute-entreprise-doit-cr%C3%A9er-ou-avoir-un-site-Web
            
            2- https://3df5e7df0cdb.ngrok.io/blog/publication/10-bonnes-raisons-d%27apprendre-%C3%A0-son-enfant-%C3%A0-coder
            
            3- https://3df5e7df0cdb.ngrok.io/blog/publication/FLASK-1.0.0
            
            Merci pour ton temps et ta perséverance dans la lecture quotidienne.
            
            Youssouf BINYOUM (digitalschools.sn)

            """
        msg = Message("Nouvelle publication sur digitalschools.sn/blog", recipients=[usermail],
                      sender='contact@digitalschools.sn')
        msg.body = content
        mail.send(msg)
        print(request.args)
    return redirect(url_for('blog.index'))

