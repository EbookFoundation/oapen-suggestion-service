PYTHONEX ?= "python"

setup-env:
ifeq ($(OS),Windows_NT)
	py -m pip install --upgrade pip
else
	$(PYTHONEX) -m pip install --upgrade pip
endif
	$(PYTHONEX) -m pip install pipenv
	$(PYTHONEX) -m pipenv install --skip-lock
	$(PYTHONEX) -m pipenv shell

seed_db:
	cd src && $(PYTHONEX) -m pipenv run python tasks/seed.py

clean_db:
	cd src && $(PYTHONEX) -m pipenv run python tasks/clean.py

clean_and_seed:
	$(MAKE) clean_db 
	$(MAKE) seed_db
	
generate_suggestions:
	cd src && $(PYTHONEX) -m pipenv run python tasks/generate_suggestions.py

run:
	$(MAKE) clean_and_seed
	$(MAKE) generate_suggestions 

run-tests:
	cd src && $(PYTHONEX) -m pipenv run pytest

refresh-items:
	cd src && $(PYTHONEX) -m pipenv run python tasks/refresh_items.py
