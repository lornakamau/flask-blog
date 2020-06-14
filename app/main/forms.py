from flask_wtf import FlaskForm 
from flask_uploads import UploadSet, IMAGES
from wtforms import SubmitField,TextAreaField,StringField,SelectField
from wtforms.validators import Required
from flask_wtf.file import FileField, FileAllowed, FileRequired

images = UploadSet('photos', IMAGES)

class PostForm(FlaskForm):
    title = StringField("Pitch Title", validators = [Required()])
    short_description = TextAreaField("Give a short decription of your post", validators=[Required()])
    post_content = TextAreaField('Post content',validators = [Required()] )
    post_pic_path = FileField('Post Image', validators=[FileRequired(),FileAllowed(images, 'Images only!')])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment_content = TextAreaField('Add a comment',validators = [Required()] )
    submit = SubmitField('Submit')

class UpdateBio(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')