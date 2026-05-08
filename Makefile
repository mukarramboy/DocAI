# Makefile
# Robust wrappers for common dev tasks that work whether you have `uv` or not.
# If `uv` is available we prefer `uv run ...`; otherwise we fall back to standard
# python invocations. This makes CI and local development more reproducible.
#
# Targets:
#   make run           - run Django dev server
#   make migrate       - run migrations
#   make makemigrations- create migrations
#   make test          - run pytest
#   make lint          - run ruff checks
#   make format        - run ruff --fix
#   make ci            - run lint then tests (useful for CI workflow)
#
# The `ci` target is intentionally simple so it composes the lint + test steps.

# Resolve appropriate command at parse time: prefer `uv` if installed.
PY := $(shell command -v uv >/dev/null 2>&1 && echo "uv run python" || echo "python")
PYTEST := $(shell command -v uv >/dev/null 2>&1 && echo "uv run python -m pytest" || echo "python -m pytest")
RUFF := $(shell command -v uv >/dev/null 2>&1 && echo "uv run ruff" || echo "python -m ruff")

.PHONY: run migrate makemigrations test lint format ci

run:
	$(PY) src/manage.py runserver

migrate:
	$(PY) src/manage.py migrate

makemigrations:
	$(PY) src/manage.py makemigrations

test:
	# Ensure src/ is on PYTHONPATH so pytest-django can import the project package 'core'
	PYTHONPATH=src DJANGO_SETTINGS_MODULE=core.settings.dev $(PYTEST)

lint:
	$(RUFF) check .

format:
	$(RUFF) check . --fix

ci: lint test
