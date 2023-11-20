##############################
Python-based stack machine
##############################

This work is inspired by Sven Havemann with his work on Generative Modelling.
The idea is to create a core stack machine in Python that can be extended simple by Pyhton.
*Core* means that it is boiled down to its bare minimum.
All the rest is down with extensions.

Sven has oriented himself at the Postscript interpreter.
Scheme is an approach to boil down Lisp to its bare minimum.
It only need 7 primitives to build up the rest of the scheme universe.

The stack machine works a follows:

#. It tokenizes its input stream
#. It executes the tokens one after each other.
    If the token is not executable, its value is put on the stack.


What is in the core
===================

Datatypes
---------

The built-in data types are:

 * ``int``: Integer numbers represented with the Python type ``int``  
 * ``float``: Float numbers
 * ``bool``
 * ``string``
 * ``symbol``: a symbol is simply an indentifier of a function or variable 
 * ``path``: a sequence of identifiers seperated by a ``.``.
 * ``function``: a object that executes a list.

Sven decided against a boolean data type.
We know from C that this works but that it also has a lot of draw backs.
All modern languages come with a boolean type.
This is why I also decided to include this type although it may work without it.

The data types 
* ``list``: represented by a pyhton list but syntactically written as a lisp list
* ``2D vector``
* ``3D vector``
can be implemented as addons and must not be included in the interpreter.

 
Commands
--------

 * ``def`` to assign a value to an identifier, with is a symbol or a path
 * ``func`` creates a function object that executes a list
 
With a path, dictionaries are created implicitly.
The command:

    5.0 origin.x def 

creates a dictionary ``origin`` and puts a key/value pair ``'x': 5.0`` in it.


What is not included
====================

Sven put a 2D an 3D vector type in his machine.
This is not necessary. 
It can be done easily with extention.
Maybe a numpy extention could solve all this.

Sven called lists *arrays*.
The term *list* is equivalent to Svens arrays.

Sven defined registers.
I think because Postscript has registers.
I don't see the difference between a register and a value assigned to a symbol.
So I do not include registers and try it only with symbols/paths.

Postscript defines scopes with ``begin`` and ``end``.
I do not have scopes yet.
But a have a pair of brackets (``[]``) left to create scopes.


Extensibility
===============

The stack machine maintains a stack of dictionaries in which the values of the symbols are stored.
Every extention can register a dictionary with name/function pairs.
The machine tries to resolve the symbol by looking in each of the dictionaries.
If it finds a value, it executes the value or puts it on the stack.


Grammar
========

The grammar is defined in an ``antlr`` file.



Examples
=========

List creation:

    ( 5.0 true "hello" )

Executable list creation:

    { dup print }

This is syntactial sugar for:

    ( dup 'print) func

Function definitaion:

    { dup mult } 'sqrt def


