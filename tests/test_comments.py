import unittest
from app.models import Post, User, Comment
from app import db

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.new_comment = Comment(comment_content = 'content')
        self.new_post = Post(title = "title", post_content= "description", short_description= "Testing testing", post_pic_path="photo_url")
        self.new_user = User(username = "lorna", email ="lorna@gmail.com", bio = "I am cool", profile_pic_path = "image_url", password = 'lorna')

        db.session.add(self.new_post)
        db.session.add(self.new_user)
        db.session.add(self.new_comment)
        db.session.commit()
        

    def tearDown(self):
        Comment.query.delete()
        Post.query.delete()
        User.query.delete()
        db.session.commit()

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment_content, 'content')

    def test_get_comments(self):
        self.new_comment.save_comment()
        get_comments = Comment.get_comments(1)
        self.assertEquals(self.new_comment.id, 1)
        