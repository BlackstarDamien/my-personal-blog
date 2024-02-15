run-server:
	python manage.py runserver

e2e:
	python manage.py test blog.tests.e2e

integration:
	python manage.py test blog.tests.integration

unit:
	python manage.py test blog.tests.unit

test-all:
	python manage.py test

make-migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

generate-static:
	python manage.py collectstatic

deps:
	pip install -r requirements.txt
