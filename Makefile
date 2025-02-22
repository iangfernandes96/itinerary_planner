.PHONY: build up down recreate-db psql migrate-up migrate-down run logs

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
	docker compose exec app alembic upgrade head

migrate-down:
	docker compose exec app alembic downgrade base

run:
	docker compose up

logs:
	docker compose logs -f

shell:
	docker compose exec app bash 