
JSMIN=python ../../hibird/jsmin.py
CSSMIN=python ../../hibird/cssmin.py

all: simple.min.css external.min.css

simple.min.css: ../yui/font-min.css element.css simple.css 
	cat $^ | ${CSSMIN} > $@
external.min.css: ../yui/font-min.css element.css external.css 
	cat $^ | ${CSSMIN} > $@

