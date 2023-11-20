all: Lexer.py

%.html: %.rst
	python -m docutils $< $@

%.py: %.g4
	antlr4 -Dlanguage=Python3 $<
