from flask import render_template,abort,redirect,url_for,request,flash
from . import main
from ..models import User, Post, Comment
from .forms import PostForm, CommentForm, UpdateBio
from .. import db,photos
from flask_login import login_required, current_user
from ..requests import get_quotes, repeat_get_quotes

@main.route('/')
def index():
    title= 'Home | SoftBlog'
    quote= get_quotes()
    quotes= repeat_get_quotes(10, get_quotes)
    posts=Posts.query.all()
    return render_template('index.html', title=title, posts=posts, quotes=quotes)

@main.route('/posts/<post_id>/<user_id>')
def posts(post_id,user_id):

    '''
    View root page function that returns the posts page and its data
    '''
    post= Post.get_post(post_id)
    user= User.get_user(user_id)
    title= post.title + ' | SoftBlog'
    return render_template('posts.html', title=title, post=post)

@main.route('/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    title = 'New Post | SoftBlog'
    form = PostForm()
    if form.validate_on_submit():
        post = Post(post_content=form.post_content.data, author=current_user, title=form.title.data, short_description=form.short_description.data, post_pic_path=form.post_pic_path.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been posted!', 'success')
        return redirect(url_for('main.posts'))

    return render_template('posts/add_post.html',title=title, post_form=form)

@main.route("/comment/<int:post_id>", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    title = 'New Comment | SoftBlog'
    form = CommentForm()
    posts = Post.query.filter_by(id = post_id).first()
    if form.validate_on_submit():
        comment = Comment(comment_content=form.comment_content.data, commenter=current_user, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.posts'))

    return render_template('posts/add_comment.html', title=title, comment_form=form, posts =posts)

@main.route('/<username>/profile')
@login_required
def profile(username):
    user = User.query.filter_by(username = username).first()
    title = current_user.username + " | Profile"
    if user is None:
        abort(404)
    posts= Post.get_user_post(user.id)
    return render_template("profile/profile.html", user = user, posts=posts, title=title)

@main.route('/<username>/bio',methods = ['GET','POST'])
@login_required
def update_bio(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)

    form = UpdateBio()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.profile',username=user.username))

    return render_template('profile/update_bio.html',form =form)

@main.route('/<username>/pic',methods= ['POST'])
@login_required
def update_pic(username):
    user = User.query.filter_by(username = username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',username=username))
