# This Makefile requires the following commands to be available:
# * python3.9
# * docker

PYTHON_VERSION=python3.9

REQUIREMENTS_BASE:=requirements/base.txt
REQUIREMENTS_TEST:=requirements/test.txt
REQUIREMENTS_DEV:=requirements/dev.txt
REQUIREMENTS_TXT:=requirements.txt

# Empty files used to keep track of installed types of virtualenvs (see rules below)
VENV_BASE=venv/.venv_base
VENV_PROD=venv/.venv_prod
VENV_TEST=venv/.venv_test
VENV_DEV=venv/.venv_dev

.PHONY: pyclean
pyclean:
	@find . -name *.pyc -delete
	@rm -rf *.egg-info build
# @rm -rf coverage.xml .coverage
# @rm -f de-customer-*.tgz

.PHONY: clean
clean: pyclean
	@rm -rf venv

# lint/black should run before lint/flake8 because it shows diff for the files to be changed
.PHONY: lint
lint: lint/black lint/flake8 lint/mypy lint/isort

.PHONY: lint/flake8
lint/flake8: $(VENV_TEST)
	@venv/bin/flake8 src

.PHONY: lint/mypy
lint/mypy: $(VENV_TEST)
	@venv/bin/mypy src

.PHONY: lint/isort
lint/isort: $(VENV_TEST)
	@venv/bin/isort --diff --check src 

.PHONY: lint/black
lint/black: $(VENV_TEST)
	@venv/bin/black --diff --check src

.PHONY: format
format: format/isort format/black

.PHONY: format/isort
format/isort: $(VENV_TEST)
	@venv/bin/isort src

.PHONY: format/black
format/black: $(VENV_TEST)
	@venv/bin/black --verbose src

$(REQUIREMENTS_TXT): | $(VENV_BASE)
	@venv/bin/pip install pip-tools
	@# see: https://github.com/jazzband/pip-tools/issues/1030 for build isolation flag
	@venv/bin/pip-compile \
		--no-emit-index-url --no-emit-trusted-host --upgrade \
		--output-file $(REQUIREMENTS_TXT) \
		--build-isolation \
		$(REQUIREMENTS_BASE)
	@echo "Successfully Updated requirements"

REVISION: VERSION?=$(shell git describe --tags --always)
REVISION: BRANCH?=$(shell git branch | grep '*' | awk '{print $$2}')
REVISION:
	@echo "$(BRANCH) $(VERSION)" > REVISION

################################################
# Setting up of different kinds of virtualenvs #
################################################
$(VENV_BASE):
	@rm -rf venv
	@$(PYTHON_VERSION) -m venv venv
	@touch $@

$(VENV_PROD): $(VENV_BASE)
# @$(MAKE) checks/requirements_txt
	@venv/bin/pip install -r $(REQUIREMENTS_TXT)
	@touch $@

$(VENV_TEST): $(VENV_PROD) $(REQUIREMENTS_TEST) REVISION
	@venv/bin/pip install -r $(REQUIREMENTS_TEST)
	@touch $@

$(REQUIREMENTS_DEV): | requirements/dev.example.txt
	@cp $| $@

$(VENV_DEV): $(VENV_PROD) $(VENV_TEST) $(REQUIREMENTS_DEV)
	@venv/bin/pip install -r $(REQUIREMENTS_DEV)
	@touch $@

.PHONY: venv
venv: $(VENV_DEV)

######################
# Django application #
######################
.PHONY: migrate
run/migrate:
	@venv/bin/python src/manage.py migrate --noinput
	@echo 'Applied migrations successfully!'

.PHONY: migrations
run/migrations: $(VENV_BASE)
	@venv/bin/python src/manage.py makemigrations

run/webserver: $(VENV_PROD)
	@venv/bin/uwsgi --ini etc/uwsgi.ini

run/devserver: $(VENV_DEV)
	@venv/bin/python src/manage.py runserver 0.0.0.0:8000

docker/compose/migrate:
	@docker-compose run web venv/bin/python src/manage.py migrate

docker/compose/migrations:
	@docker-compose run web venv/bin/python src/manage.py makemigrations

docker/compose/build:
	@docker-compose build --no-cache web

docker/compose/up:
	@docker-compose up

docker/compose/unittest:
	@docker-compose exec web venv/bin/python -m pytest src/tests