run:
	uv run python src/manage.py runserver

migrate:
	uv run python src/manage.py migrate

makemigrations:
	uv run python src/manage.py makemigrations

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff check . --fix
