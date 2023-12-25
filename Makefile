all: readme.html

%.html: %.rst
	python -m docutils $< $@

upload:
	rm -rf dist
	python -m build
	twine upload dist/*
