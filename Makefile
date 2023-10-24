MANAGE_PY := python manage.py

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
	$(MANAGE_PY) runserver localhost:8000
