make build:
	python3 manage.py migrate;
	python3 manage.py migrate --run-syncdb;
	echo "from django.contrib.auth import get_user_model;  User = get_user_model(); User.objects.create_superuser('root', 'admin@admin.com', 'root')" | python3 manage.py shell
make run:
		python3 manage.py runserver;
make clean:
	# worning this deletes untracked files
	git clean -fdX
make user:
	echo "from django.contrib.auth import get_user_model;  User = get_user_model(); User.objects.create_superuser('root', 'admin@admin.com', 'root')" | python3 manage.py shell
make test:
	python3 manage.py test

make data:
	echo "from django.contrib.auth import get_user_model;  User = get_user_model(); User.objects.create_user('user1', 'user1@user.com')" | python3 manage.py shell
	echo "from socialapp import models; from django.contrib.auth import get_user_model; User = get_user_model(); user1 = User.objects.get(email='user1@user.com'); models.Author.objects.create(github='https://api.github.com/users/jejewittt',localuser=user1 ,displayName='user1' ,image='https://avatars0.githubusercontent.com/u/25070007?v=4' , feed='https://api.github.com/users/jejewittt/events')" | python3 manage.py shell
	echo "from socialapp import models; user1 = models.Author.objects.get(displayName='user1'); models.Post.objects.create(author=user1,title='public', source='http://1.1',origin='http://1.1',contentType='PUBLIC',description='PUBLIC',content='PUBLIC',unlisted=False,published='2020-03-13',visibility='PUBLIC')" | python3 manage.py shell
	echo "from socialapp import models; user1 = models.Author.objects.get(displayName='user1'); models.Post.objects.create(author=user1,title='PRIVATE Author', source='http://1.1',origin='http://1.1',contentType='PRIVATE',description='PRIVATE',content='PRIVATE',unlisted=False,published='2020-03-13',visibility='PRIVATE')" | python3 manage.py shell
	echo "from socialapp import models; user1 = models.Author.objects.get(displayName='user1'); models.Post.objects.create(author=user1,title='PRIVATE', source='http://1.1',origin='http://1.1',contentType='PRIVATE',description='PRIVATE',content='PRIVATE',unlisted=False,published='2020-03-13',visibility='PRIVATE')" | python3 manage.py shell
	echo "from socialapp import models; user1 = models.Author.objects.get(displayName='user1'); models.Post.objects.create(author=user1,title='FRIENDS', source='http://1.1',origin='http://1.1',contentType='FRIENDS',description='FRIENDS',content='FRIENDS',unlisted=False,published='2020-03-13',visibility='FRIENDS')" | python3 manage.py shell
	echo "from socialapp import models; user1 = models.Author.objects.get(displayName='user1'); models.Post.objects.create(author=user1,title='public', source='http://1.1',origin='http://1.1',contentType='PUBLIC',description='PUBLIC',content='PUBLIC',unlisted=True,published='2020-03-13',visibility='PUBLIC')" | python3 manage.py shell
	echo "from socialapp import models; user1 = models.Author.objects.get(displayName='user1'); models.Post.objects.create(author=user1,title='PRIVATE Author', source='http://1.1',origin='http://1.1',contentType='PRIVATE',description='PRIVATE',content='PRIVATE',unlisted=True,published='2020-03-13',visibility='PRIVATE')" | python3 manage.py shell
	echo "from socialapp import models; user1 = models.Author.objects.get(displayName='user1'); models.Post.objects.create(author=user1,title='PRIVATE', source='http://1.1',origin='http://1.1',contentType='PRIVATE',description='PRIVATE',content='PRIVATE',unlisted=True,published='2020-03-13',visibility='PRIVATE')" | python3 manage.py shell
	echo "from socialapp import models; user1 = models.Author.objects.get(displayName='user1'); models.Post.objects.create(author=user1,title='FRIENDS', source='http://1.1',origin='http://1.1',contentType='FRIENDS',description='FRIENDS',content='FRIENDS',unlisted=True,published='2020-03-13',visibility='FRIENDS')" | python3 manage.py shell
