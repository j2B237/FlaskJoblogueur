# ******************* ADMINISTRATION MODULE ****************************** #
# ** Created by Yossep
# ** github: https://github.com/j2B237/
# ** Project : Joblogueur
# ** Description:
#
# Within this module we have many functions designed to help admin or moderator
# on his daily blogger work.
# Example of Methods :
# CRUD for post, category, moderator
# Update comment status
# Check status of user requests
# ************************************************************************ #


# Third party import
import os
import secrets
from flask import (Blueprint, redirect, render_template, url_for, flash, request, escape)
from flask_login import login_required, logout_user, current_user
from PIL import Image

# Local import
from FlaskApp.models import Moderator, Post, Request, Category, Comment
from FlaskApp.forms import CategoryForm, PostForm, ModeratorForm, UpdateModeratorForm
from FlaskApp import db, bcrypt, app
from FlaskApp.auth import send_mail

# Construct a blueprint for Back Office
bp = Blueprint('admin', __name__, url_prefix='/admin')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/upload', picture_fn)

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path, quality=100)

    return picture_fn


@bp.route('/')
@login_required
def index():
    return render_template("admin/index.html", title="Joblogueur back office")


@bp.route('/notifications')
@login_required
def list_all_notifications():
    if current_user.is_admin:
        page = request.args.get('page', 1, type=int)
        notifications = Request.query.order_by(Request.date_posted.desc()).paginate(per_page=5, page=page)
        return render_template("admin/notifications.html", title="Notifications Joblogueur",
                               notifications=notifications)

    return redirect(url_for('admin.index'))


@bp.route('/post/create', methods=['POST', 'GET'])
@login_required
def create_post():
    categories = Category.query.all()
    form = PostForm()

    if request.method == 'POST':
        search_post = Post.query.filter_by(title=form.title.data).first()

        if search_post:
            flash("Une publication de titre existe deja", "danger")
        else:
            if form.Not_Publish.data == 'Oui':
                display_or_not = True
            else:
                display_or_not = False

            search_category = Category.query.filter_by(category_name=request.form['categorie']).first()
            category_id = search_category.id

            img_title = save_picture(form.img_title.data)
            img_h1 = save_picture(form.img_h1.data)
            img_h2 = save_picture(form.img_h2.data)
            img_h3 = save_picture(form.img_h3.data)
            img_h4 = save_picture(form.img_h4.data)
            img_h5 = save_picture(form.img_h5.data)
            img_h6 = save_picture(form.img_h6.data)
            img_h7 = save_picture(form.img_h7.data)
            img_h8 = save_picture(form.img_h8.data)
            img_h9 = save_picture(form.img_h9.data)

            new_post = Post(title=form.title.data,
                            introduction=form.introduction.data,
                            p_intro=form.p_intro.data,
                            img_title=img_title,
                            img_h1=img_h1,
                            h1=form.h1.data,
                            p_h1=form.p_h1.data,
                            img_h2=img_h2,
                            h2=form.h2.data,
                            p_h2=form.p_h1.data,
                            img_h3=img_h3,
                            h3=form.h3.data,
                            p_h3=form.p_h3.data,
                            img_h4=img_h4,
                            h4=form.h4.data,
                            p_h4=form.p_h4.data,
                            img_h5=img_h5,
                            h5=form.h5.data,
                            p_h5=form.p_h5.data,
                            img_h6=img_h6,
                            h6=form.h6.data,
                            p_h6=form.p_h6.data,
                            img_h7=img_h7,
                            h7=form.h7.data,
                            p_h7=form.p_h7.data,
                            img_h8=img_h8,
                            h8=form.h8.data,
                            p_h8=form.p_h8.data,
                            img_h9=img_h9,
                            h9=form.h9.data,
                            p_h9=form.p_h9.data,
                            h10=form.h10.data,
                            p_h10=form.p_h10.data,
                            conclusion=form.conclusion.data,
                            p_conclusion=form.p_conclusion.data,
                            moderator_id=current_user.id,
                            category_id=category_id,
                            display_or_not=display_or_not
                            )
            db.session.add(new_post)
            db.session.commit()

            flash("Publication créée avec success", "success")
            return redirect(url_for("admin.list_all_post"))

    return render_template("admin/new_post.html", title="Nouvelle publication - Joblogueur",
                           form=form, categories=categories)


@bp.route('/post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def post(post_id):
    categories = Category.query.all()
    # search post filter by title
    search_post = Post.query.get(post_id)
    search_moderator = Moderator.query.get(search_post.moderator_id)
    image_file = url_for('static', filename='upload/'+str(search_post.img_title))
    url_back_to = request.environ.get('HTTP_REFERER')

    return render_template("admin/post.html", title='{}'.format(search_post.title.replace(' ', '-')),
                           post=search_post, categories=categories, moderator=search_moderator,
                           image=image_file, url_back_to=url_back_to)


@bp.route('/edit/post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def edit_post(post_id):
    categories = Category.query.all()
    search_post = Post.query.get(post_id)
    status = 'Non'

    if search_post.display_or_not:
        status = 'Oui'

    form = PostForm()
    if request.method == 'POST':

        if form.Not_Publish.data == 'Oui':
            display_or_not = True
        else:
            display_or_not = False

        search_category = Category.query.filter_by(category_name=request.form['categorie']).first()
        category_id = search_category.id

        # Creation et enrégistrement d'images
        img_post = save_picture(form.img_title.data)
        img_h1 = save_picture(form.img_h1.data)
        img_h2 = save_picture(form.img_h2.data)
        img_h3 = save_picture(form.img_h3.data)
        img_h4 = save_picture(form.img_h4.data)
        img_h5 = save_picture(form.img_h5.data)
        img_h6 = save_picture(form.img_h6.data)
        img_h7 = save_picture(form.img_h7.data)
        img_h8 = save_picture(form.img_h8.data)
        img_h9 = save_picture(form.img_h9.data)

        search_post.title = form.title.data
        search_post.introduction = form.introduction.data
        search_post.p_intro = form.p_intro.data
        search_post.img_title = img_post

        search_post.img_h1 = img_h1
        search_post.h1 = form.h1.data
        search_post.p_h1 = form.p_h1.data

        search_post.img_h2 = img_h2
        search_post.h2 = form.h2.data
        search_post.p_h2 = form.p_h2.data

        search_post.img_h3 = img_h3
        search_post.h3 = form.h3.data
        search_post.p_h3 = form.p_h3.data

        search_post.img_h4 = img_h4
        search_post.h4 = form.h4.data
        search_post.p_h4 = form.p_h4.data

        search_post.img_h5 = img_h5
        search_post.h5 = form.h5.data
        search_post.p_h5 = form.p_h5.data

        search_post.img_h6 = img_h6
        search_post.h6 = form.h6.data
        search_post.p_h6 = form.p_h6.data

        search_post.img_h7 = img_h7
        search_post.h7 = form.h7.data
        search_post.p_h7 = form.p_h7.data

        search_post.img_h8 = img_h8
        search_post.h8 = form.h8.data
        search_post.p_h8 = form.p_h8.data

        search_post.img_h9 = img_h9
        search_post.h9 = form.h9.data
        search_post.p_h9 = form.p_h9.data

        search_post.h10 = form.h10.data
        search_post.p_h10 = form.p_h10.data

        search_post.conclusion = form.conclusion.data
        search_post.p_conclusion = form.p_conclusion.data
        search_post.moderator_id = current_user.id
        search_post.category_id = category_id
        search_post.display_or_not = display_or_not

        db.session.commit()
        flash("Publication modifiée avec succès", "success")
        return redirect(url_for('admin.post', post_id=post_id))

    elif request.method == 'GET':

        form.title.data = search_post.title
        form.introduction.data = search_post.introduction
        form.p_intro.data = search_post.p_intro
        form.img_title.data = search_post.img_title

        form.img_h1.data = search_post.img_h1
        form.h1.data = search_post.h1
        form.p_h1.data = search_post.p_h1

        form.img_h2.data = search_post.img_h2
        form.h2.data = search_post.h2
        form.p_h2.data = search_post.p_h2

        form.img_h3.data = search_post.img_h3
        form.h3.data = search_post.h3
        form.p_h3.data = search_post.p_h3

        form.img_h4.data = search_post.img_h4
        form.h4.data = search_post.h4
        form.p_h4.data = search_post.p_h4

        form.img_h5.data = search_post.img_h5
        form.h5.data = search_post.h5
        form.p_h5.data = search_post.p_h5

        form.img_h6.data = search_post.img_h6
        form.h6.data = search_post.h6
        form.p_h6.data = search_post.p_h6

        form.img_h7.data = search_post.img_h7
        form.h7.data = search_post.h7
        form.p_h7.data = search_post.p_h7

        form.img_h8.data = search_post.img_h8
        form.h8.data = search_post.h8
        form.p_h8.data = search_post.p_h8

        form.img_h9.data = search_post.img_h9
        form.h9.data = search_post.h9
        form.p_h9.data = search_post.p_h9

        form.img_h10.data = search_post.img_h10
        form.h10.data = search_post.h10
        form.p_h10.data = search_post.p_h10

        form.conclusion.data = search_post.conclusion
        form.p_conclusion.data = search_post.p_conclusion
        form.Not_Publish.data = status

    return render_template('admin/edit_post.html', title="Edition publication - Joblogueur",
                           form=form, categories=categories)


@bp.route('/delete/post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get(int(post_id))
    if post_to_delete:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Publication supprimée avec succès", "success")
        return redirect(url_for('admin.list_all_post'))
    else:
        flash("Publication n'existe pas", "info")
    return redirect(url_for('admin.list_all_post'))


@bp.route('/posts')
@login_required
def list_all_post():

    page = request.args.get('page', 1, type=int)
    author = Moderator.query.get(int(current_user.id))
    author_id = author.id

    if author_id:
        posts = Post.query.filter_by(moderator_id=int(author_id)).\
            order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
        return render_template("admin/posts.html", title="Publications - Joblogueur", posts=posts)
    else:
        return render_template("admin/posts.html", title="Publications - Joblogueur")


@bp.route('/category/create', methods=['POST', 'GET'])
@login_required
def create_category():
    form = CategoryForm()

    if form.validate_on_submit():
        # Verification avant insertion
        search_category = Category.query.filter_by(category_name=form.category_name.data).first()
        if search_category:
            flash("Ce nom de categorie existe déja", "danger")
        else:
            new_category = Category(category_name=form.category_name.data, color=form.color.data)
            db.session.add(new_category)
            db.session.commit()
            flash("Nouvelle categorie créée avec succès", "success")
            return redirect(url_for('admin.list_all_categories'))

    return render_template("admin/new_category.html", title="Nouvelle catégorie", form=form)


@bp.route('/category/save-create', methods=['POST'])
@login_required
def save_create_another():
    form = CategoryForm()
    if request.method == 'POST':
        # Verification avant insertion
        search_category = Category.query.filter_by(category_name=form.category_name.data).first()
        if search_category:
            flash("Ce nom de categorie existe déja", "danger")
        else:
            another_categorie = Category(category_name=form.category_name.data)
            db.session.add(another_categorie)
            db.session.commit()
            flash("Nouvelle categorie créée avec succès", "success")
            return redirect(url_for('admin.create_category'))

    return render_template("admin/new_category.html", title="Nouvelle catégorie", form=form)


@bp.route('/edit/category/<int:category_id>', methods=['POST', 'GET'])
@login_required
def edit_category(category_id):
    search_category = Category.query.get(int(category_id))

    form = CategoryForm()

    if form.validate_on_submit():

        # Verification avant insertion
        search_category.category_name = form.category_name.data
        search_category.color = form.color.data
        db.session.commit()
        flash("Modification effectuée avec succès", "success")
        return redirect(url_for('admin.list_all_categories'))

    elif request.method == "GET":
        form.category_name.data = search_category.category_name
        form.color.data = search_category.color

    return render_template("admin/edit_category.html", form=form)


@bp.route('/category/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    search_category = Category.query.get(int(category_id))
    if request.method == 'POST':
        db.session.delete(search_category)
        db.session.commit()
    return redirect(url_for("admin.list_all_categories"))


@bp.route('/categories')
@login_required
def list_all_categories():

    page = request.args.get('page', 1, type=int)
    categories = Category.query.order_by(Category.date_posted.desc()).paginate(per_page=3, page=page)
    pub_per_cat = []

    if current_user.is_admin:
        # Pour chaque categorie
        for categorie in categories.items:
            # créer un objet dict qui comprend pour clé le nom de la categorie et pour valeur le nombre de publication
            objet = {"category_id": categorie.id,
                     "category_name": categorie.category_name,
                     "date_posted": categorie.date_posted,
                     "posts": len(categorie.posts)
                     }
            pub_per_cat.append(objet)

        return render_template("admin/categories.html", title="Categories Joblogueur",
                               pub_per_cat=pub_per_cat, categories=categories)

    return redirect(url_for('admin.index'))


@bp.route('/archives')
@login_required
def list_all_archive():
    author = Moderator.query.get(int(current_user.id))
    author_id = author.id

    if author_id:
        posts = Post.query.filter_by(moderator_id=author_id).all()
        comments = Comment.query.filter_by(approved_or_not=False).all()
        return render_template("admin/archives.html", title="Archives Joblogueur",
                               posts=posts, comments=comments)
    else:
        return render_template("admin/archives.html", title="Archives Joblogueur")


@bp.route('/archives/<int:comment_id>', methods=['POST', 'GET'])
@login_required
def change_comment_status(comment_id):
    if request.method == 'POST':
        comment = Comment.query.get(int(comment_id))
        response = comment.approved_comment_status
        if response:
            db.session.commit()
    return redirect(url_for('admin.list_all_archive'))


@bp.route('/archives/delete/comment/<int:comment_id>', methods=['POST', 'GET'])
@login_required
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get(int(comment_id))
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for('admin.list_all_archive'))


@bp.route('/moderator/create', methods=['POST', 'GET'])
@login_required
def create_moderator():
    form = ModeratorForm()

    if form.validate_on_submit():
        search_email = Moderator.query.filter_by(email=form.email.data).first()
        if search_email:
            flash("Cet utilisateur existe déja", "danger")
        else:
            if form.img_file.data:
                moderator_pic = save_picture(form.img_file.data)
                img_file = moderator_pic

            username = form.username.data
            email = form.email.data
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            new_moderator = Moderator(username=username, email=email, password=hashed_password,
                                      is_admin=False, img_file=img_file)

            db.session.add(new_moderator)
            db.session.commit()
            flash("Moderateur enrégistré avec succès", "success")
            return redirect(url_for('admin.list_all_moderators'))

    return render_template("admin/new_moderator.html", title="Nouveau membre - Joblogueur", form=form)


@bp.route('/moderator/add/<username>',  methods=['POST', 'GET'])
@login_required
def add_moderator(username):
    form = ModeratorForm()
    request_to_add = Request.query.filter_by(sender=username).first()

    if form.validate_on_submit():
        search_moderator = Moderator.query.filter_by(email=form.email.data).first()

        if search_moderator:
            flash("Cet email existe déja", "danger")
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = Moderator(username=form.username.data, email=form.email.data,
                                 password=hashed_password, is_admin=False)
            db.session.add(new_user)
            request_to_add.validate_or_not = True
            db.session.commit()

            moderator = {
                "username": form.username.data,
                "user_mail": form.email.data
            }

            send_mail(moderator)
            flash("Moderateur ajouté dans la base de donnée", "success")
            return redirect(url_for('admin.list_all_notifications'))

    form.username.data = escape(username)
    form.email.data = request_to_add.email
    form.password.data = ""

    return render_template('admin/add_moderator.html', title="Nouveau membre - Digital Schools Blog",
                           form=form)


@bp.route('/moderator/profil/<moderator_username>', methods=['POST', 'GET'])
@login_required
def moderator(moderator_username):

    page = request.args.get('page', 1, type=int)
    profil = Moderator.query.filter_by(username=moderator_username).first()
    profil_posts_comments = []
    if profil:

        profil_posts = Post.query.join(Moderator).filter(Post.moderator_id == profil.id).paginate(per_page=4, page=page)

        for post in profil_posts.items:
            objet_comments = {
                                'post_id': post.id,
                                'total': len(post.comments)
                            }
            profil_posts_comments.append(objet_comments)

    url_back_to = request.environ.get('HTTP_REFERER')

    image_file = url_for('static', filename='upload/' + profil.img_file)
    return render_template('admin/moderator_profil.html', titre='Profil moderateur - Joblogueur',
                           moderator=profil, posts=profil_posts,
                           profil_posts_comments=profil_posts_comments, image=image_file, url_back_to=url_back_to)


@bp.route('/moderators')
@login_required
def list_all_moderators():
    page = request.args.get('page', 1, type=int)
    if current_user.is_admin:
        moderators = Moderator.query.filter_by(is_admin=False).paginate(per_page=4, page=page)
        return render_template("admin/moderators.html", title="Moderateurs - Joblogueur", moderators=moderators)
    return redirect(url_for('admin.index'))


@bp.route('/account')
@login_required
def account():
    moderator_id = current_user.id
    search_moderator = Moderator.query.get(moderator_id)

    profil_posts_comments = []
    page = request.args.get('page', 1, type=int)
    profil_posts = Post.query.join(Moderator).filter(Post.moderator_id == moderator_id).paginate(per_page=4, page=page)

    for post in profil_posts.items:
        objet_comments = {
            'post_id': post.id,
            'total': len(post.comments)
        }
        profil_posts_comments.append(objet_comments)

    image_file = url_for('static', filename='upload/' + search_moderator.img_file)
    url_back_to = request.environ.get('HTTP_REFERER')
    return render_template("admin/account.html", title="Compte Administrateur - Joblogueur",
                           moderator=search_moderator, posts=profil_posts,
                           profil_posts_comments=profil_posts_comments,
                           image=image_file, url_back_to=url_back_to)


@bp.route('/account/update', methods=['POST', 'GET'])
@login_required
def update_account():
    moderator_agent = Moderator.query.get(current_user.id)

    form = UpdateModeratorForm()
    if request.method == 'POST':
        if form.img_file.data:
            profile_pic = save_picture(form.img_file.data)
            moderator_agent.img_file = profile_pic

        moderator_agent.username = form.username.data
        moderator_agent.email = form.email.data
        moderator_agent.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()

        flash("Modification effectuée avec succès", "success")
        return redirect(url_for('admin.account'))

    elif request.method == 'GET':
        form.username.data = moderator_agent.username
        form.email.data = moderator_agent.email
    image_file = url_for('static', filename='upload/' + moderator_agent.img_file)
    return render_template("admin/update_account.html", title="Modification compte - Joblogueur",
                           form=form, image=image_file)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog.index'))
