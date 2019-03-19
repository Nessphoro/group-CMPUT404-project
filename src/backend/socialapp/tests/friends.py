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

    #Test to check Friend Requests
	def testSendFriendRequest(self):
		self.author1.send_friend_request(self.author2)
		friendResult = self.author1.friends.all()
		self.assertTrue(self.author2 in friendResult)
		requestResult = self.author2.friend_requests.all()
		self.assertTrue(self.author1 in requestResult)

	def testSendFriendRequestwithPendingRequest(self):
		self.author2.send_friend_request(self.author4)
		self.author4.send_friend_request(self.author2)
		friendResult = self.author4.friends.all()
		self.assertTrue(self.author2 in friendResult)
		requestResult = self.author4.friend_requests.all()
		self.assertTrue(self.author2 not in requestResult)

	def testRemoveFriend(self):
		self.author1.remove_from_friends(self.author3)
		friendResult = self.author1.friends.all()
		self.assertTrue(self.author3 not in friendResult)
		self.assertTrue(self.author1.is_follower(self.author3))

	def testAcceptFriendRequest(self):
		self.author1.send_friend_request(self.author2)
		self.author2.accept_friend_request(self.author1)
		friendResult = self.author2.friends.all()
		self.assertTrue(self.author1 in friendResult)
	
	def testDeclineFriendRequest(self):
		self.author1.send_friend_request(self.author4)
		self.author4.decline_friend_request(self.author1)
		requestResult = self.author4.friend_requests.all()
		self.assertTrue(self.author1 not in requestResult)