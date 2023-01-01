install: ## [DEVELOPMENT] Install the API dependencies
	virtualenv env; \
	source env/bin/activate; \
	pip install -r requirements.txt
	@echo "Done, run '\033[0;31msource env/bin/activate\033[0m' to activate the virtual environment"
