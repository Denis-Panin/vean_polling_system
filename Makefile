MANAGE = src/manage.py

run:
	$(MANAGE) runserver

new-migrate:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

shell:
	$(MANAGE) shell_plus --print-sql

freeze:
	pip freeze > requirements.txt

lint:
	flake8 ./src
