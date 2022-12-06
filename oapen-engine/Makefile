PYTHONEX ?= "python"
PYTHONPATH = "$(CURDIR)/src"
PYTHON = PYTHONPATH="$(PYTHONPATH)" $(PYTHONEX)

setup-env:
ifeq ($(OS),Windows_NT)
	py -m pip install --upgrade pip
else
	$(PYTHON) -m pip install --upgrade pip
endif
	$(PYTHON) -m pip install pipenv
	$(PYTHON) -m pipenv install --skip-lock
	$(PYTHON) -m pipenv shell

seed_db:
	cd src && $(PYTHON) -m pipenv run python tasks/seed.py

clean_db:
	cd src && $(PYTHON) -m pipenv run python tasks/clean.py

clean_and_seed:
	$(MAKE) clean_db 
	$(MAKE) seed_db
	
generate_suggestions:
	cd src && $(PYTHON) -m pipenv run python tasks/generate_suggestions.py

run:
	$(MAKE) clean_and_seed
	$(MAKE) generate_suggestions 

run-tests:
	cd src && $(PYTHON) -m pipenv run pytest

refresh-items:
	cd src && $(PYTHON) -m pipenv run python tasks/refresh_items.py

test-stopword-generation:
	cd src && $(PYTHON) -m pipenv run python model/stopwords_processor.py
