import markdown2 
from flask import render_template,abort,redirect,url_for,request,flash
from . import main
from ..models import User, Post, Comment, MailList
from .forms import PostForm, CommentForm, UpdateBio, SubscribeForm
from .. import db,photos
from flask_login import login_required, current_user
from ..requests import get_quotes, repeat_get_quotes
from werkzeug import secure_filename
from ..email import subscribe_message
from flask_paginate import Pagination, get_page_parameter

@main.route('/', methods=['GET', 'POST'])
def index():
    title= 'Home | SoftBlog'
    quote= get_quotes()
    quotes= repeat_get_quotes(10, get_quotes)
    all_posts=Post.get_posts()
    page = request.args.get('page', 1, type=int)
    posts=all_posts.paginate(per_page=6)
    form= SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        new_mail = MailList(email = email)

        db.session.add(new_mail)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('index.html', title=title, posts=posts, quotes=quotes, subscribe_form=form)

@main.route('/Posts/<post_id>',methods=['GET', 'POST'])
@login_required
def posts(post_id):
    post= Post.get_post(post_id)
    if post is None:
        abort(404)
    format_post = markdown2.markdown(post.post_content,extras=["code-friendly", "fenced-code-blocks"])
    all_comments = Comment.get_comments(post.id)
    print(all_comments)
    comment_form=CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(comment_content = comment_form.comment_content.data, commenter=current_user, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.posts', post_id = post.id))
    subscribe_form= SubscribeForm()
    if subscribe_form.validate_on_submit():
        email = form.email.data
        new_mail = MailList(email = email)

        db.session.add(new_mail)
        db.session.commit()
        return redirect(url_for('main.posts', post_id=post.id))
    title= post.title + ' | SoftBlog'
    return render_template('posts.html', title=title, post=post, comments=all_comments, comment_form=comment_form, format_post=format_post, subscribe_form=subscribe_form)

@main.route('/Post/<post_id>')
def single_post(post_id):
    post= Post.get_post(post_id)
    if post is None:
        abort(404)
    format_post = markdown2.markdown(post.post_content,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('posts.html', post_id=post.id, format_post=format_post)

@main.route('/New-post', methods=['GET', 'POST'])
@login_required
def new_post():
    title = 'New Post | SoftBlog'
    heading = "New Post"
    form = PostForm()
    if form.validate_on_submit() and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path=f'photos/{filename}'
        post = Post(post_content=form.post_content.data, author=current_user, title=form.title.data, short_description=form.short_description.data, post_pic_path=path)
        db.session.add(post)
        db.session.commit()
        mailList = MailList.query.all()
        subscribers = []
        for subscriber in mailList:
            subscribers.append(subscriber.email)
        for subscriber in subscribers:
            subscribe_message("New post on SoftBlog!","email/subscribe", subscriber, user = current_user, post=post, heading=heading)
        flash('Your post has been posted!', 'success')
        return redirect(url_for('main.index'))

    return render_template('posts/add_post.html',title=title, post_form=form)

@main.route('/Posts/<post_id>/update', methods=['GET', 'POST'] )
@login_required
def update_post(post_id):
    post= Post.get_post(post_id)
    heading = "Update post"
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit() and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path=f'photos/{filename}'
        post.post_content=form.post_content.data
        post.author=current_user
        post.title=form.title.data
        post.short_description=form.short_description.data
        post.post_pic_path=path
        db.session.commit()
        mailList = MailList.query.all()
        subscribers = []
        for subscriber in mailList:
            subscribers.append(subscriber.email)
        for subscriber in subscribers:
            subscribe_message("A post on SoftBlog has been updated!","email/subscribe", subscriber, user = current_user, heading=heading)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.posts', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.post_content.data = post.post_content
        form.short_description.data = post.short_description
    title = "Update Post | SoftBlog"
    return render_template('posts/add_post.html',title=title, post_form=form, heading=heading)

@main.route('/Posts/<post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post= Post.get_post(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.profile', username = current_user.username))

@main.route("/Comment/<int:post_id>", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    title = 'New Comment | SoftBlog'
    form = CommentForm()
    post = Post.query.filter_by(id = post_id).first()
    if form.validate_on_submit():
        comment = Comment(comment_content=form.comment_content.data, commenter=current_user, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.posts', post_id = post.id))

    return render_template('posts/add_comment.html', title=title, comment_form=form, post=post)

@main.route('/Comment/<post_id>/<comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(post_id,comment_id):
    post= Post.get_post(post_id)
    comment = Comment.get_comment(comment_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment successfully deleted!', 'success')
    return redirect(url_for('main.posts', post_id=post.id))

@main.route('/<username>/Profile')
def profile(username):
    user = User.query.filter_by(username = username).first()
    title = user.username + " | Profile"
    if user is None:
        abort(404)
    posts= Post.get_user_post(user.id)
    return render_template("profile/profile.html", user = user, posts=posts, title=title)

@main.route('/<username>/Update-bio',methods = ['GET','POST'])
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

@main.route('/<username>/Update-pic',methods= ['POST'])
@login_required
def update_pic(username):
    user = User.query.filter_by(username = username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',username=username))
