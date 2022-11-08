PYTHONEX := "python"
PIPEX := "pip"

setup-env:
ifeq ($(OS),Windows_NT)
	py -m pip install --upgrade pip
else
	$(PYTHONEX) -m pip install --upgrade pip
endif
	$(PIPEX) install pipenv
	pipenv install
	pipenv shell

seed_db:
	cd src && pipenv run python tasks/seed.py

clean_db:
	cd src && pipenv run python tasks/clean.py
	
run:
	cd src && pipenv run python main.py

run-tests:
	cd src && pipenv run pytest