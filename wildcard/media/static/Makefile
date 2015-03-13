
SHELL = /bin/sh
GRUNT=./node_modules/.bin/grunt
BOWER = ./node_modules/bower/bin/bower

bootstrap:
	npm install
	$(BOWER) install

prod:
	$(GRUNT) prod
	cp build/bundle.js integration.js
