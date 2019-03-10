make build:
	python3 manage.py migrate;
	echo "from django.contrib.auth import get_user_model;  User = get_user_model(); User.objects.create_superuser('root', 'admin@admin.com', 'root')" | python3 manage.py shell
make run:
		python3 manage.py runserver;
make clean:
	# worning this deletes untracked files
	git clean -fdX
make user:
	echo "from django.contrib.auth import get_user_model;  User = get_user_model(); User.objects.create_superuser('root', 'admin@admin.com', 'root')" | python3 manage.py shell
