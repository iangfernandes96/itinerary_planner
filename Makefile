.PHONY: build up down recreate-db psql migrate-up migrate-down logs install-hooks frontend-install frontend-build

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

recreate-db:
	docker compose down -v
	docker compose up -d

psql:
	docker compose exec db psql -U itinerary_user -d itinerary_db

migrate-up:
	docker compose exec backend alembic upgrade head

migrate-down:
	docker compose exec backend alembic downgrade base

logs:
	docker compose logs -f

shell-backend:
	docker compose exec backend bash

shell-frontend:
	docker compose exec frontend sh

install-hooks:
	pip install -r requirements.txt
	pre-commit install

frontend-install:
	cd frontend && npm install

frontend-build:
	cd frontend && npm run build
