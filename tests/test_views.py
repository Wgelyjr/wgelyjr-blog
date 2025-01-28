import unittest
from blog import *

class TestBlog(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    # Home page test
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    # Login page test
    def test_loginpage(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
    
    # New user page test
    def test_newuserpage(self):
        response = self.client.get('/newuser')
        self.assertEqual(response.status_code, 200)
    
    # New post page test
    def test_newpostpage(self):
        response = self.client.get('/newpost')
        self.assertEqual(response.status_code, 200)
    
    # Posts page test
    def test_postspage(self):
        response = self.client.get('/posts/:id')
        self.assertEqual(response.status_code, 200)
    
    # Edit post page test
    def test_editpostpage(self):
        response = self.client.get('/editpost/:id')
        self.assertEqual(response.status_code, 200)
    
    # Delete post page test
    def test_deletepostpage(self):
        response = self.client.get('/deletepost/:id')
        self.assertEqual(response.status_code, 302)
    
    # New comment page test
    def test_newcommentpage(self):
        response = self.client.get('/newcomment/:postid')
        self.assertEqual(response.status_code, 200)
    
    # About page test
    def test_aboutpage(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
    
    # Template injection test
    def test_templateinjection(self):
        postindex = db.session.query(Posts).order_by(Posts.id.desc())
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('{{postindex}}', self.client.context['index'])
    
    # Error handler test
    def test_errorhandler(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('404: Page not found.' in self.client.text)
