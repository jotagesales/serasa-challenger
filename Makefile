clean:
	@echo "Execute cleaning ..."
	rm -f *.pyc
	rm -f .coverage
	rm -f coverage.xml


test: clean
	pytest --cov=. tests

coverage: clean
	pytest tests --cov=. --cov-report=html

dependencies:
	docker compose up -d db

down:
	docker compose down

migrate:
	python manage.py migrate

runserver: dependencies migrate
	python manage.py runserver
