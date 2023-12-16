PORT ?= 8000

full-test:
	poetry run pytest --show-capture=stdout --showlocals -vv
light-test:
	poetry run pytest --no-summary --disable-pytest-warnings
lint:
	poetry run flake8 page_analyzer
check: light-test lint
push: check
	git push


install:
	poetry install
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl --force
test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

dev:
	poetry run flask --app page_analyzer:app --debug run
server:
	sudo service postgresql start

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
start-server:
	gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app

freeze:
	poetry export --without-hashes --format=requirements.txt > requirements.txt
up: freeze
	docker-compose up
