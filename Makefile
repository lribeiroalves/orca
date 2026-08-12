.PHONY: requirements run clear-cache

requirements:
	pip-compile requirements.in
	pip install -r requirements.txt

run:
	flask run

clear-cache:
	find . -type d -name "__pycache__" -exec rm -r {} +