FROM python:3
EXPOSE 8000
WORKDIR /root/app
ADD . /root/app
RUN pip install -r requirements.txt
WORKDIR /root/app/src/backend

RUN rm -rf db.sqlite3 && python manage.py makemigrations && python manage.py migrate --run-syncdb
ENV PRODUCTION=true
CMD python manage.py runserver 0.0.0.0:8000