FROM python:3
EXPOSE 8000
VOLUME [ "/external" ]
WORKDIR /root/app
ADD requirements.txt /root/app/requirements.txt
RUN pip install -r requirements.txt
ADD . /root/app
WORKDIR /root/app/src/backend

ENV PRODUCTION=true
RUN python manage.py makemigrations
CMD python manage.py migrate --run-syncdb && python manage.py runserver 0.0.0.0:8000