from django.test import TestCase
from django.contrib.auth import get_user_model
from socialapp import models;

class TestPrivacy(TestCase):

	@classmethod
	def setUpTestData(cls):
		User = get_user_model();
		cls.user1 = User.objects.create_user('user1', 'user1@user.com')
		cls.user2 = User.objects.create_user('user2', 'user2@user.com')
		cls.user3 = User.objects.create_user('user3', 'user2@user.com')
		cls.user4 = User.objects.create_user('user4', 'user2@user.com')

		cls.author1 = models.Author.objects.create(github='https://api.github.com/users/jejewittt',
									localuser=cls.user1,
									displayName='user1',
									image='https://avatars0.githubusercontent.com/u/25070007?v=4', 
									feed='https://api.github.com/users/jejewittt/events')

		cls.author2 = models.Author.objects.create(github='https://api.github.com/users/jejewittt',
									localuser=cls.user2,
									displayName='user2',
									image='https://avatars0.githubusercontent.com/u/25070007?v=4', 
									feed='https://api.github.com/users/jejewittt/events')
		cls.author3 = models.Author.objects.create(github='https://api.github.com/users/jejewittt',
									localuser=cls.user3,
									displayName='user2',
									image='https://avatars0.githubusercontent.com/u/25070007?v=4', 
									feed='https://api.github.com/users/jejewittt/events')
		cls.author4 = models.Author.objects.create(github='https://api.github.com/users/jejewittt',
									localuser=cls.user4,
									displayName='user2',
									image='https://avatars0.githubusercontent.com/u/25070007?v=4', 
									feed='https://api.github.com/users/jejewittt/events')
		cls.author1.friends.add(cls.author3)
		cls.author3.friends.add(cls.author1)
		cls.author4.friends.add(cls.author3)
		cls.author3.friends.add(cls.author4)


		cls.public_post = models.Post.objects.create(author=cls.author1,title='public', 
									source='http://1.1',
									origin='http://1.1',contentType='PUBLIC',
									description='PUBLIC',content='PUBLIC',
									unlisted=False,published='2019-03-13',
									visibility='PUBLIC')
		cls.public_post_unlisted = models.Post.objects.create(author=cls.author1,title='public', 
											source='http://1.1',
											origin='http://1.1',contentType='PUBLIC',
											description='PUBLIC',content='PUBLIC',
											unlisted=True,published='2019-03-13',
											visibility='PUBLIC')
		cls.private_post = models.Post.objects.create(author=cls.author1,title='PRIVATE', 
									source='http://1.1',
									origin='http://1.1',contentType='PRIVATE',
									description='PRIVATE',content='PRIVATE',
									unlisted=False,published='2019-03-13',
									visibility='PRIVATE')
		cls.private_post_unlisted = models.Post.objects.create(author=cls.author1,title='PRIVATE', 
									source='http://1.1',
									origin='http://1.1',contentType='PRIVATE',
									description='PRIVATE',content='PRIVATE',
									unlisted=True,published='2019-03-13',
									visibility='PRIVATE')
		cls.private_post_add = models.Post.objects.create(author=cls.author1,title='PRIVATE', 
									source='http://1.1',
									origin='http://1.1',contentType='PRIVATE',
									description='PRIVATE',content='PRIVATE',
									unlisted=False,published='2019-03-13',
									visibility='PRIVATE')
		cls.private_post_unlisted_add = models.Post.objects.create(author=cls.author1,title='PRIVATE', 
									source='http://1.1',
									origin='http://1.1',contentType='PRIVATE',
									description='PRIVATE',content='PRIVATE',
									unlisted=True,published='2019-03-13',
									visibility='PRIVATE')
		cls.private_post_add.visibleTo.add(cls.author3)
		cls.private_post_unlisted_add.visibleTo.add(cls.author3)


		cls.friends_post = models.Post.objects.create(author=cls.author1,title='FRIENDS', 
									source='http://1.1',
									origin='http://1.1',contentType='PUBLIC',
									description='PUBLIC',content='PUBLIC',
									unlisted=False,published='2019-03-13',
									visibility='FRIENDS')
		cls.friends_post_unlisted = models.Post.objects.create(author=cls.author1,title='FRIENDS', 
											source='http://1.1',
											origin='http://1.1',contentType='PUBLIC',
											description='PUBLIC',content='PUBLIC',
											unlisted=True,published='2019-03-13',
											visibility='FRIENDS')
		cls.fof_post = models.Post.objects.create(author=cls.author1,title='FOAF', 
									source='http://1.1',
									origin='http://1.1',contentType='PUBLIC',
									description='PUBLIC',content='PUBLIC',
									unlisted=False,published='2019-03-13',
									visibility='FOAF')
		cls.fof_post_unlisted = models.Post.objects.create(author=cls.author1,title='FOAF', 
											source='http://1.1',
											origin='http://1.1',contentType='PUBLIC',
											description='PUBLIC',content='PUBLIC',
											unlisted=True,published='2019-03-13',
											visibility='FOAF')


		cls.fof_post = models.Post.objects.create(author=cls.author1,title='FOAF', 
									source='http://1.1',
									origin='http://1.1',contentType='PUBLIC',
									description='PUBLIC',content='PUBLIC',
									unlisted=False,published='2019-03-13',
									visibility='FOAF')
		cls.fof_post_unlisted = models.Post.objects.create(author=cls.author1,title='FOAF', 
											source='http://1.1',
											origin='http://1.1',contentType='PUBLIC',
											description='PUBLIC',content='PUBLIC',
											unlisted=True,published='2019-03-13',
											visibility='FOAF')
		cls.public_post_origin = models.Post.objects.create(author=cls.author1,title='SERVERONLY', 
									source='http://127.0.0.1:8000',
									origin='http://127.0.0.1:8000',contentType='PUBLIC',
									description='PUBLIC',content='PUBLIC',
									unlisted=False,published='2019-03-13',
									visibility='SERVERONLY')
		cls.public_post_origin_unlisted = models.Post.objects.create(author=cls.author1,title='SERVERONLY', 
											source='http://127.0.0.1:8000',
											origin='http://127.0.0.1:8000',contentType='PUBLIC',
											description='PUBLIC',content='PUBLIC',
											unlisted=True,published='2019-03-13',
											visibility='SERVERONLY')
		cls.public_post_origin_bad = models.Post.objects.create(author=cls.author1,title='public', 
									source='http://127.0.0.2:8000',
									origin='http://127.0.0.2:8000',contentType='SERVERONLY',
									description='PUBLIC',content='PUBLIC',
									unlisted=False,published='2019-03-13',
									visibility='SERVERONLY')
		cls.public_post_origin_unlisted_bad = models.Post.objects.create(author=cls.author1,title='SERVERONLY', 
											source='http://127.0.0.2:8000',
											origin='http://127.0.0.2:8000',contentType='PUBLIC',
											description='PUBLIC',content='PUBLIC',
											unlisted=True,published='2019-03-13',
											visibility='SERVERONLY')
	def testPublic(self):
		self.assertTrue(self.author2.post_permission(self.public_post))
		result = self.author2.get_public()
		self.assertTrue(result.filter(id=self.public_post.id).exists())
	def testPublicUnlisted(self):
		result = self.author2.get_public()
		self.assertFalse(result.filter(id=self.public_post_unlisted.id).exists())
		self.assertTrue(self.author2.post_permission(self.public_post))
	def testPrivate(self):
		result = self.author1.get_my_feed()
		self.assertTrue(result.filter(id=self.private_post.id).exists())
		self.assertTrue(self.author1.post_permission(self.private_post))
		self.assertFalse(self.author2.post_permission(self.private_post))
		self.assertFalse(self.author3.post_permission(self.private_post))
		result = self.author2.get_private()
		self.assertFalse(result.filter(id=self.private_post.id).exists())

	def testPrivateUnlisted(self):
		result = self.author1.get_my_feed()
		self.assertTrue(result.filter(id=self.private_post_unlisted.id).exists())

		result = self.author2.get_private()
		self.assertFalse(result.filter(id=self.private_post_unlisted.id).exists())

		self.assertTrue(self.author1.post_permission(self.private_post_unlisted))
		self.assertFalse(self.author2.post_permission(self.private_post_unlisted))
		self.assertFalse(self.author3.post_permission(self.private_post_unlisted))

	def testPrivate_add(self):
		result = self.author3.get_private()
		self.assertTrue(result.filter(id=self.private_post_add.id).exists())
		self.assertTrue(self.author1.post_permission(self.private_post_add))
		self.assertFalse(self.author2.post_permission(self.private_post_add))
		self.assertTrue(self.author3.post_permission(self.private_post_add))
		result = self.author2.get_private()
		self.assertFalse(result.filter(id=self.private_post_add.id).exists())

	def testPrivateUnlisted_add(self):
		result = self.author3.get_private()
		self.assertFalse(result.filter(id=self.private_post_unlisted_add.id).exists())
		self.assertTrue(self.author1.post_permission(self.private_post_unlisted_add))
		self.assertFalse(self.author2.post_permission(self.private_post_unlisted_add))
		self.assertTrue(self.author3.post_permission(self.private_post_unlisted_add))

	def testFriends(self):
		self.assertFalse(self.author2.post_permission(self.friends_post))
		self.assertTrue(self.author3.post_permission(self.friends_post))
		result = self.author3.get_posts_of_friends()
		self.assertTrue(result.filter(id=self.friends_post.id).exists())
		result = self.author2.get_posts_of_friends()
		self.assertFalse(result.filter(id=self.friends_post.id).exists())
	def testFriendsUnlisted(self):
		result = self.author2.get_posts_of_friends()
		self.assertFalse(result.filter(id=self.friends_post_unlisted.id).exists())
		self.assertFalse(self.author2.post_permission(self.friends_post_unlisted))
		result = self.author3.get_posts_of_friends()
		self.assertFalse(result.filter(id=self.friends_post_unlisted.id).exists())
		self.assertTrue(self.author3.post_permission(self.friends_post_unlisted))

	def testFOF(self):
		self.assertFalse(self.author2.post_permission(self.fof_post))
		self.assertTrue(self.author3.post_permission(self.fof_post))
		self.assertTrue(self.author4.post_permission(self.fof_post))
		result = self.author3.get_posts_of_friends_of_friends()
		self.assertTrue(result.filter(id=self.fof_post.id).exists())
		result = self.author2.get_posts_of_friends_of_friends()
		self.assertFalse(result.filter(id=self.fof_post.id).exists())
	def testFOFUnlisted(self):
		result = self.author2.get_posts_of_friends_of_friends()
		self.assertFalse(result.filter(id=self.fof_post_unlisted.id).exists())
		self.assertFalse(self.author2.post_permission(self.fof_post_unlisted))
		self.assertTrue(self.author4.post_permission(self.fof_post_unlisted))
		result = self.author3.get_posts_of_friends_of_friends()
		self.assertFalse(result.filter(id=self.fof_post_unlisted.id).exists())
		self.assertTrue(self.author3.post_permission(self.fof_post_unlisted))

	def testOrigin(self):
		self.assertTrue(self.author1.post_permission(self.public_post_origin))
		self.assertFalse(self.author1.post_permission(self.public_post_origin_bad))
		result = self.author1.get_server()
		self.assertTrue(result.filter(id=self.public_post_origin.id).exists())
		result = self.author1.get_server()
		self.assertFalse(result.filter(id=self.public_post_origin_bad.id).exists())
	def testOriginUnlisted(self):
		self.assertTrue(self.author1.post_permission(self.public_post_origin_unlisted))
		self.assertFalse(self.author1.post_permission(self.public_post_origin_unlisted_bad))
		result = self.author2.get_server()
		self.assertFalse(result.filter(id=self.public_post_origin_unlisted.id).exists())
		result = self.author2.get_server()
		self.assertFalse(result.filter(id=self.public_post_origin_unlisted_bad.id).exists())

	def testIsMe(self):
		self.assertTrue(self.author1.is_me(self.author1))
		self.assertFalse(self.author1.is_me(self.author2))
