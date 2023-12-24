all: Lexer.py

%.py: %.g4
	antlr4 -Dlanguage=Python3 $<
