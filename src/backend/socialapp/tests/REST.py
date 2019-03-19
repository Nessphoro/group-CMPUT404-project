from django.test import TestCase
from django.contrib.auth import get_user_model
from socialapp import models

from rest_framework.test import APIClient
from socialapp import urls

class TestREST(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user1 = User.objects.create_user('user1', 'user1@user.com')
        cls.author1 = models.Author.objects.create(github='https://api.github.com/users/jejewittt',
									localuser=cls.user1,
									displayName='user1',
									image='https://avatars0.githubusercontent.com/u/25070007?v=4', 
									feed='https://api.github.com/users/jejewittt/events')                               
        cls.public_post = models.Post.objects.create(author=cls.author1,title='public', 
									source='http://1.1',
									origin='http://1.1',contentType='PUBLIC',
									description='PUBLIC',content='PUBLIC',
									unlisted=False,published='2019-03-13',
									visibility='PUBLIC')
        cls.public_post_comment = models.Comment.objects.create(author=cls.author1,post=cls.public_post,
                                    comment="test",contentType='PUBLIC',published='2019-03-19')

    def testGetHome(self):
        client = APIClient()
        response = client.get('')
        self.assertEqual(response.status_code, 200)

    def testGetAuthor(self):
        client = APIClient()
        path = self.author1.get_absolute_url()
        response = client.get(path)
        self.assertEqual(response.status_code, 200)

    def testGetPost(self):
        client = APIClient()
        path = self.public_post.get_absolute_url()
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
 
    def testGetEditComment(self):
        client = APIClient()
        path = self.public_post_comment.get_absolute_url()
        response = client.get(path)
        self.assertEqual(response.status_code, 200)

    def testGetCreateComment(self):
        client = APIClient()
        path = self.public_post.get_absolute_url()
        path = "/Comment" + path[5:] + "create"
        response = client.get(path)
        self.assertEqual(response.status_code, 200)

    """
    def testPostPost(self):
        client = APIClient()
        path = "/Post/create/"

        #author = self.author1
        #title = "test"
        #source = 'http://1.1'
        #origin = 'http://1.1'
        #contentType = 'PUBLIC'
        #description = 'testpostpost'
        #content = 'does it work?'
        #unlisted = False
        #published = '2019-03-19'
        #visibility = 'PUBLIC'

        responce = client.post(path, {'author': 'author1', 'title': 'test', 'source': 'http://1.1', 'origin': 'http://1.1', 
        'contentType': 'PUBLIC', 'description': 'testpostpost', 'content': 'does it work?', 'unlisted': 'False', 
        'published': '2019-03-19', 'visibility': 'PUBLIC'})

        print('\n')
        print(responce)
        print('\n')
    """
    #login = self.client.login(username='user1')