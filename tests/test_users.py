import unittest
from app.models import User
from app import db

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(username = "lorna", email ="lorna@gmail.com", bio = "I am cool", profile_pic_path = "image_url", password = 'lorna')
        db.session.add(self.new_user)
        db.session.commit()

    def tearDown(self):
        User.query.delete()
        db.session.commit()
 
    def test_password_setter(self):
        self.assertTrue(self.new_user.pass_secure is not None)

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('lorna'))

    def test_save_user(self):
        self.new_user.save_user()
        self.assertTrue(len(User.query.all())>0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_user.username, 'lorna')
        self.assertEquals(self.new_user.email, 'lorna@gmail.com')
        self.assertEquals(self.new_user.bio, 'I am cool')
        self.assertEquals(self.new_user.profile_pic_path, 'image_url')
        self.assertTrue(self.new_user.verify_password('lorna'))


    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password 