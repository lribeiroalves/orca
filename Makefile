.PHONY: requirements run clear-cache venv

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
FLASK := $(VENV)/bin/flask

venv:
	python3 -m venv $(VENV)

requirements: venv
	. $(VENV)/bin/activate && python -m pip install --upgrade pip pip-tools
	. $(VENV)/bin/activate && pip-compile requirements.in
	. $(VENV)/bin/activate && pip install -r requirements.txt

run: venv
	. $(VENV)/bin/activate && FLASK_APP=app FLASK_ENV=development flask run --host=0.0.0.0 --port=5000

clear-cache:
	find . -type d -name "__pycache__" -exec rm -r {} +