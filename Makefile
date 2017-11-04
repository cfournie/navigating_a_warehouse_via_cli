python_files := find . -path '*/.*' -prune -o -name '*.py' -print0

install:
	pip install -e .[dev]

autopep8:
	@echo 'Auto Formatting...'
	@$(python_files) | xargs -0 autopep8 --jobs 0 --in-place --aggressive --global-config setup.cfg

lint:
	@echo 'Linting...'
	@pylint --rcfile=pylintrc setup.py navigate_warehouse_via_cli tests scripts
	@pycodestyle .

autolint: autopep8 lint

run_tests: clean
	py.test --durations=10 .
