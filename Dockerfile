FROM python:3
EXPOSE 8000
VOLUME [ "/external" ]
WORKDIR /root/app
ADD . /root/app
RUN pip install -r requirements.txt
WORKDIR /root/app/src/backend

ENV PRODUCTION=true
RUN python manage.py makemigrations
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000