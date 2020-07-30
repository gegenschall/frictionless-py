.PHONY: all docs list install format lint readme release templates test version


PACKAGE := $(shell grep '^PACKAGE =' setup.py | cut -d '"' -f2)
VERSION := $(shell head -n 1 $(PACKAGE)/assets/VERSION)
LEAD := $(shell head -n 1 LEAD.md)


all: list

docs:
	python scripts/docs.py

format:
	black $(PACKAGE) tests

install:
	pip install --upgrade -e .[aws,bigquery,ckan,dataflows,elastic,gsheet,html,ods,pandas,server,spss,sql,tsv,dev]
	test -f '.git/hooks/pre-commit' || cp .gitverify .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

lint:
	black $(PACKAGE) tests --check
	pylama $(PACKAGE) tests
	# mypy $(PACKAGE) --ignore-missing-imports

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

release:
	git checkout master && git pull origin && git fetch -p
	@git log --pretty=format:"%C(yellow)%h%Creset %s%Cgreen%d" --reverse -20
	@echo "\nReleasing v$(VERSION) in 10 seconds. Press <CTRL+C> to abort\n" && sleep 10
	git commit -a -m 'v$(VERSION)' && git tag -a v$(VERSION) -m 'v$(VERSION)'
	git push --follow-tags

templates:
	sed -i -E "s/@(\w*)/@$(LEAD)/" .github/issue_template.md
	sed -i -E "s/@(\w*)/@$(LEAD)/" .github/pull_request_template.md

test:
	make lint
	pytest --cov ${PACKAGE} --cov-report term-missing --cov-fail-under 50


version:
	@echo $(VERSION)
