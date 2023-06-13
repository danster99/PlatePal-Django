MANAGE_PY := python PlatePalDjango/manage.py
FRONTEND_DIR := lcp-frontend

# Commands
.PHONY: shell
shell:  ## Open a Django shell.
	$(MANAGE_PY) shell_plus --ipython

# Administration
.PHONY: setup
setup: migrate collectstatic superuser  ## Setup a local environment to start development.

.PHONY: makemigrations
makemigrations:  ##Start makemigrations
	$(MANAGE_PY) makemigrations

.PHONY: migrate
migrate:  ## Start Django database migrations in verbose mode.
	$(MANAGE_PY) migrate -v 2

.PHONY: collectstatic
collectstatic:  ## Collect Django static files.
	$(MANAGE_PY) collectstatic --noinput

.PHONY: superuser
superuser:  ## Create a superuser for development.
	$(MANAGE_PY) createdevelopmentsuperuser

.PHONY: runserver
runserver:  ## Run a auto reloading Django development server.
	$(MANAGE_PY) runserver 0.0.0.0:8000

rundramatiq: ## Run a auto reloading dramatiq server for background jobs
	 PYTHONPATH=$(PWD)/src $(MANAGE_PY) rundramatiq --reload --processes 2 --threads 2

## Formatting
.PHONY: format
format: isort-fix black-fix fe-format  ## Call all code formatters.

.PHONY: isort-fix
isort-fix:  ## Let the isort formatter fix the imports.
	isort $(PWD)

.PHONY: black-fix
black-fix:  ## Let the black formatter fix your code styling.
	black $(PWD)

## Linting
.PHONY: lint
lint: black-check isort-check markdownlint ruff bandit poetry-check fe-lint  ## Call all the code linters.

.PHONY: markdownlint
markdownlint:
	markdownlint-cli2 .

.PHONY: ruff
ruff:  ## Let ruff check for code styling issues.
		ruff check --quiet $(PWD)

.PHONY: isort-check
isort-check:  ## Let isort check for import issues.
	isort --check $(PWD)

.PHONY: black-check
black-check:  ## Let black check for code styling issues.
	black --check $(PWD)

.PHONY: bandit
bandit:  ## Let bandit check for secuirty issues in your code.
	bandit --configfile pyproject.toml -r $(PWD)

.PHONY: poetry-check
poetry-check:  ## Validate the poetry configuration in pyproject.toml.
	poetry check -n -v

## Frontend
.PHONY: fe-frontend
fe-runserver:  ## Starts a development webserver for the frontend application.[]
	cd $(FRONTEND_DIR)
	npm run runserver

.PHONY: fe-format
fe-format:
	cd $(FRONTEND_DIR)
	npm run format

.PHONY: fe-lint
fe-lint:
	cd $(FRONTEND_DIR)
	npm run format-check
	npm run lint
	npm run type-check

.PHONY: fe-build
fe-build:
	cd $(FRONTEND_DIR)
	npm run build
