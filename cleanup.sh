poetry run pycodestyle .
poetry run isort --profile=black .
poetry run black .
poetry run pylint */
