from flask import render_template,abort,redirect,url_for,request,flash
from . import main
from ..models import User, Post, Comment
from .forms import PostForm
from .. import db,photos
from flask_login import login_required, current_user

# Views
@main.route('/')
def home():

    '''
    View root page function that returns the home page and its data
    '''
    posts = Post.get_posts()
    title= 'Home'
    return render_template('home.html', title=title, posts=posts)

@main.route('/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    title = 'New Post | Blog'
    form = PostForm()
    if form.validate_on_submit():
        post = Post(post_content=form.post_content.data, author=current_user, title=form.title.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been posted!', 'success')
        return redirect(url_for('main.home'))

    return render_template('posts/add_post.html',title=title, pitch_form=form)

@main.route("/comment/<int:post_id>", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    title = 'New Comment | Blog'
    form = CommentForm()
    posst = Post.query.filter_by(id = post_id).first()
    if form.validate_on_submit():
        comment = Comment(comment_content=form.comment_content.data, user=current_user, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.home'))

    return render_template('posts/add_comment.html', title=title, comment_form=form, categories=categories, pitch=pitch)