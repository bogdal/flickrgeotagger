
install:
	pip install -r deploy/requirements.txt --upgrade

test:
	python manage.py test
