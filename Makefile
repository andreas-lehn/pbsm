all: readme.html

%.html: %.rst
	python -m docutils $< $@
