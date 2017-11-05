install:
	pip install -e .[dev]

autopep8:
	@echo 'Auto Formatting...'
	@autopep8 --in-place --aggressive --global-config setup.cfg **/*.py scripts/*

lint:
	@echo 'Linting...'
	@pylint --rcfile=pylintrc setup.py navigate_warehouse_via_cli tests scripts
	@pycodestyle .

autolint: autopep8 lint

test:
	py.test -vv .
