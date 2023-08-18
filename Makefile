init: install-deps

install-deps:
	@pip install --upgrade pip setuptools wheel
	@pip install --upgrade poetry
	@poetry install
	@pre-commit install --hook-type commit-msg
	@pre-commit run --all-files
