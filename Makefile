include .env
export

app-dir = app
bot-dir = bot

all:
	uv run -m $(bot-dir)



.PHONY lint:
lint:
	echo "Running ruff..."
	uv run ruff check --config pyproject.toml --diff $(app-dir)

.PHONY format:
format:
	echo "Running ruff check with --fix..."
	uv run ruff check --config pyproject.toml --fix --unsafe-fixes $(app-dir)

	echo "Running ruff..."
	uv run ruff format --config pyproject.toml $(app-dir)

	echo "Running isort..."
	uv run isort --settings-file pyproject.toml $(app-dir)

.PHONE mypy:
mypy:
	echo "Running MyPy..."
	uv run mypy --config-file pyproject.toml --package $(app-dir).$(bot-dir)


.PHONY freeze: sync
freeze:
	uv export --quiet --format requirements-txt --no-dev --extra uvloop --output-file $(app-dir)\requirements.txt

.PHONY create-revision:
create-revision:
	cd $(app-dir) && uv run alembic revision --autogenerate -m "$(message)"

.PHONY upgrade-revision:
upgrade-revision:
	cd $(app-dir) && uv run alembic upgrade "$(revision)"

.PHONY downgrade-revision:
downgrade-revision:
	cd $(app-dir) && uv run alembic downgrade "$(revision)"

.PHONY current-revision:
current-revision:
	cd $(app-dir) && uv run alembic current

.PHONY create-init-revision:
create-init-revision:
	cd $(app-dir) && uv run alembic revision --autogenerate -m 'Initial' --rev-id 000000000000
