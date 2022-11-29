setup-env:
ifeq ($(OS),Windows_NT)
	py -m pip install --upgrade pip
else
	python -m pip install --upgrade pip
endif
	pip install pipenv
	pipenv install
	pipenv shell

seed_db:
	cd src && pipenv run python tasks/seed.py

clean_db:
	cd src && pipenv run python tasks/clean.py

clean_and_seed:
	$(MAKE) clean_db 
	$(MAKE) seed_db
	
generate_suggestions:
	cd src && pipenv run python tasks/generate_suggestions.py

run:
	$(MAKE) clean_and_seed
	$(MAKE) generate_suggestions 

run-tests:
	cd src && pipenv run pytest

refresh-items:
	cd src && pipenv run python tasks/refresh_items.py