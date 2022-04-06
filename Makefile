.DEFAULT_GOAL=all

.PHONY: format
format:
	poetry run black -l 79 src/ tests/

.PHONY: test
test:
	poetry run pytest tests/

.PHONY: coverage
coverage:
	poetry run pytest --cov-report term-missing --cov=src tests/

.PHONY: lint
lint:
	poetry run pylint src/

.PHONY: typehint
typehint:
	poetry run mypy --ignore-missing-imports src/

.PHONY: test-suite
test-suite: lint typehint coverage

.PHONY: build
build:
	poetry build

.PHONY: all
all: test-suite build

.PHONY: clean
clean:
	rm -rf .mypy_cache/ .pytest_cache/ dist/ .coverage