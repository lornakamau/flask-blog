from flask import render_template
from . import main

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('home.html')

@main.route('/new-pitch', methods=['GET', 'POST'])
@login_required
def new_pitch():
    title = 'New Pitch | Pitch'
    form = PitchForm()
    if form.validate_on_submit():
        post = Pitch(post_content=form.post_content.data, author=current_user, title=form.title.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been posted!', 'success')
        return redirect(url_for('main.posts'))

    return render_template('posts/create_post.html',title=title, pitch_form=form)