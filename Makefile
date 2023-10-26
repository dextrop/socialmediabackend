# Init vars
MAKEFILE := $(lastword $(MAKEFILE_LIST))
BASENAME := $(shell basename "$(PWD)")
SHELL := /bin/bash

.PHONY: help
all: help
help: Makefile
	@echo
	@echo " Commands:"
	@echo
	@sed -n 's/^##//p' $< | sed -e 's/^/ /' | sort
	@echo


## Migrate Database
migrate:
	python manage.py makemigrations backendapp && python manage.py migrate

install:
	pip install -r requirements.txt

## Create Super User
createsuperuser:
	python manage.py createsuperuser

## Create Super User
run:
	python manage.py runserver