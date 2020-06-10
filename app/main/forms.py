from flask_wtf import FlaskForm 
from wtforms import SubmitField,TextAreaField,StringField,SelectField
from wtforms.validators import Required

class PostForm(FlaskForm):
    title = StringField("Pitch Title", validators = [Required()])
    post_content = TextAreaField('What pitch do you want to share?',validators = [Required()] )
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment_content = TextAreaField('Add a comment',validators = [Required()] )
    submit = SubmitField('Submit')

class UpdateBio(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')