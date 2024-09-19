.PHONY:install
install:
	poetry install


.PHONY:install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install 


.PHONY: lint
lint:
	poetry run pre-commit run --all-files


.PHONY:migrate
migrate:
	poetry run python -m core.manage migrate


.PHONY:migrations
migrations:
	poetry run python -m core.manage makemigrations


.PHONY:collectstatic
collectstatic:
	poetry run python -m core.manage collectstatic


.PHONY:runserver
runserver:
	poetry run python -m core.manage runserver_plus


.PHONY:run-huey
run-huey:
	poetry run python -m core.manage run_huey


.PHONY:superuser
superuser:
	poetry run python -m core.manage createsuperuser


.PHONY:book-fixtures
book-fixtures:
	poetry run python -m core.manage loaddata --app books books


.PHONY:author-fixtures
author-fixtures:
	poetry run python -m core.manage loaddata --app books authors


.PHONY:works-fixtures
works-fixtures:
	poetry run python -m core.manage loaddata --app works work


.PHONY:series-fixtures
series-fixtures:
	poetry run python -m core.manage loaddata --app works series


.PHONY:setup
setup: install migrations migrate install-pre-commit ;


.PHONY:push-update
push-update: migrations migrate collectstatic ;


.PHONY:load-fixtures
load-fixtures: works-fixtures series-fixtures author-fixtures  book-fixtures ;