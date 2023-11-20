all: StackMachineLexer.py

%.html: %.rst
	python -m docutils $< $@

%.py: %.g4
	antlr -Dlanguage=Python3 $<
