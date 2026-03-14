.PHONY: help install migrate run db-start db-stop superuser shell test clean

help:
	@echo "Команды:"
	@echo "  make install    - установить зависимости"
	@echo "  make db-start   - запустить PostgreSQL"
	@echo "  make db-stop    - остановить PostgreSQL"
	@echo "  make migrate    - создать и применить миграции"
	@echo "  make superuser  - создать админа"
	@echo "  make run        - запустить сервер"
	@echo "  make shell      - Django shell"
	@echo "  make test       - запустить тесты"

install:
	pip install -r requirements.txt

db-start:
	cd ../storage && docker-compose up -d

db-stop:
	cd ../storage && docker-compose down

migrate:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsuperuser

run:
	python manage.py runserver

shell:
	python manage.py shell

test:
	python manage.py test

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
