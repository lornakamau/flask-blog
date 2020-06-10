from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model): #db.Model helps connect our class to our database
    __tablename__ = 'users' #gives tables in our database proper names
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    comments = db.relationship('Comment', backref='user',lazy="dynamic")
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    posts = db.relationship('Post',backref = 'author',lazy = "dynamic")

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute') #raises an attribute error when we try to access the password

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)

    def __repr__(self): #defines how the user object will be constructed when the class is called
        return f'USER {self.username}'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment_content = db.Column(db.String())
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    def save_comment(self):
            db.session.add(self)
            db.session.commit()

    @classmethod
    def get_comments(cls,id):
            comments = Comment.query.filter_by(pitch_id=id).all()
            return comments
                
    def __repr__(self):
        return f'COMMENT {self.comment_content}'

class Post(db.Model):
        __tablename__ = 'posts'
        id = db.Column(db.Integer,primary_key = True)
        title = db.Column(db.String())
        post_content = db.Column(db.String())
        posted = db.Column(db.DateTime,default=datetime.utcnow)
        author_id = db.Column(db.Integer,db.ForeignKey("users.id"))
        comments = db.relationship("Comment", backref ='user', lazy = "dynamic")

        def save_post(self):
                db.session.add(self)
                db.session.commit()

        @classmethod
        def get_user_pitch(cls,id):
                user_pitches = Pitch.query.filter_by(pitcher_id = id).order_by(Pitch.posted.desc())
                return user_pitches

        @classmethod
        def get_posts(cls):
                all_posts = Post.query.order_by(Post.posted.desc())
                return all_posts

        @classmethod
        def get_post_id(cls,id):
                post_id = Pitch.query.filter_by(id = id).order_by(Post.id.desc()) 
                return post_id


        def __repr__(self):
                return f"POST {self.title}"