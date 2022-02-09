FROM python:3.8

# key from django.core.management.utils.get_random_secret_key
ENV SECRET_KEY=django-insecure-4a-l)zxb%!3)3q*a%62!yaa74#ds6@qe%@@n-4-%r_zcnsn60!
ENV DEBUG=True
ENV DATABASE_URL=sqlite:////app/db.sqlite3
ENV DJANGO_SETTINGS_MODULE=poketrainers.settings
ENV WORKERS=3

COPY . /app/
WORKDIR /app/
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py get_pokemons

EXPOSE 8000
CMD gunicorn poketrainers.wsgi --bind 0:8000 --workers=$WORKERS