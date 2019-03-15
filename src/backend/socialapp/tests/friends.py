from django.test import TestCase
from django.contrib.auth import get_user_model
from socialapp import models;

class TestFriends(TestCase):

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