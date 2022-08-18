.EXPORT_ALL_VARIABLES:
COMPOSE_FILE ?= docker-compose.yml
COMPOSE_PROJECT_NAME ?= pg-back
SOURCE_FILES ?= server

DOTENV_BASE_FILE ?= .env
-include $(DOTENV_BASE_FILE)

MIGRATIONS_DB_CONFIG = server/alembic.ini


.PHONY: install-packages
install-packages:
	pip install pipenv && pipenv install --deploy --system --ignore-pipfile


.PHONY: docker-build
docker-build:
	@docker build \
		--tag=pg-back \
		--file=docker/Dockerfile \
		--build-arg BUILD_RELEASE=dev \
		.

.PHONY: docker-up
docker-up:
	docker-compose -f $(COMPOSE_FILE) --env-file=.env up --remove-orphans -d
	docker-compose ps

.PHONY: docker-down
docker-down:
	docker-compose down

.PHONY: docker-prune
docker-prune:
	docker container prune -f
	docker volume prune -f

.PHONY: docker-logs
docker-logs:
	docker-compose logs --follow

.PHONY: docker-bash
docker-bash:
	docker-compose -f $(COMPOSE_FILE) exec backend bash

.PHONY: lint-bandit
lint-bandit:
	bandit --ini .bandit --recursive

.PHONY: lint-black
lint-black:
	black --check --diff ./$(SOURCE_FILES)

.PHONY: lint-flake8
lint-flake8:
	flake8 ./$(SOURCE_FILES)

.PHONY: lint-isort
lint-isort:
	isort --check-only --diff ./$(SOURCE_FILES)


.PHONY: lint
lint: lint-black lint-flake8 lint-isort  lint-bandit

.PHONY: fmt
fmt:
	isort .
	black .

.PHONY: test
test:
	docker-compose -f $(COMPOSE_FILE) exec backend pytest tests/.

.PHONY: migrate
migrate:
	docker-compose exec backend alembic --config $(MIGRATIONS_DB_CONFIG) upgrade head

.PHONY: migrations
migrations:
	docker-compose exec backend alembic --config $(MIGRATIONS_DB_CONFIG) revision --autogenerate --message auto


.PHONY: alembic-history
alembic-history:
	docker-compose exec backend alembic --config $(MIGRATIONS_DB_CONFIG) history


.PHONY: alembic-merge-heads
alembic-merge-heads:
	docker-compose exec backend alembic --config $(MIGRATIONS_DB_CONFIG) merge heads

.PHONY: service
service:
	python3 server/main.py



