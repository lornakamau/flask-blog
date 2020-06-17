import unittest
from app.models import Post
from app import db

class PitchModelTest(unittest.TestCase):
    def setUp(self):
        self.new_post = Post(title = "title", post_content= "description", short_description= "Testing testing", post_pic_path="photo_url")
        db.session.add(self.new_post)
        db.session.commit()

    def tearDown(self):
        Post.query.delete()
        db.session.commit()

    def test_save_post(self):
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all())>0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_post.title, 'title')
        self.assertEquals(self.new_post.post_content, 'description')
        self.assertEquals(self.new_post.short_description, 'Testing testing')
