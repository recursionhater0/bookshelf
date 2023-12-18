CONTAINER_NAME ?= web

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

restart: down build up

logs:
	docker compose logs -f

migrate:
	docker compose exec $(CONTAINER_NAME) python manage.py migrate

createsuperuser:
	docker compose exec $(CONTAINER_NAME) python manage.py createsuperuser
