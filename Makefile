.PHONY: configs
configs:
	cp configs.sample.py configs.py
	cp .env.example .env

.PHONY: superuser
superuser:
	DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --no-input --username=admin --email=admin@admin.com

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: statics
statics:
	python manage.py collectstatic --no-input

checkmigrations:
	python manage.py makemigrations --check --no-input --dry-run

gunicorn:
	gunicorn --bind 0.0.0.0:8000 bitArticles.wsgi:application

init: migrate statics superuser

