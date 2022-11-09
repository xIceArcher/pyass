.PHONY: all lint lint-check test

CMD:=poetry run
PYMODULE:=pyass

all: lint test

lint:
	$(CMD) black .
	$(CMD) isort .
	$(CMD) pyright .

lint-check:
	$(CMD) black . --check
	$(CMD) isort . --check-only
	$(CMD) pyright . --warnings

test:
	$(CMD) pytest --cov=$(PYMODULE) --cov-report=xml
