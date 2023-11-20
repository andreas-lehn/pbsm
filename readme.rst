##############################
Python-based stack machine
##############################

This work is inspired by Sven Havemanns work on `Generative Modelling <https://en.wikipedia.org/wiki/Generative_Modelling_Language>`_.
The idea is to create a stack machine in Python that is minimalistic but easy to extended.
*Minimalistic* means that it is boiled down to its bare minimum.
All the rest is down with extensions written in Python

Sven has oriented himself at the Postscript interpreter and so is this state machine.
Because it is based on Python, there are a few differences to the Postscript stack machine:

 * All objects on the stack are Python objects.
 * Postscript uses ``()`` to denote strings.
   PBSM uses the standard Python syntax for strings: ``'``, ``"`` or ``"""`` enclose a valid string.
 * Postscript use ```/``` to push a literal on the stack. PBSM uses ``'`` instead.
   This makes the syntax more consistent and uses less characters with special meaning.


Datatypes
===================

PBSM uses standard object types of Python: ``int``, ``float``, ``string``, ``bool`` and ``list``.
It introduces the following types:

 * ``Marker`` to denote the start of a list/executable list.
 * ``Symbol`` for a symbolic name.
 * ``Reference`` references a symbol
 * ``Procedure`` represents an executable list.

 
Commands
=========

The core interpreter comes with a few commands only.
These are:

 * ``[`` together with ``]`` creates the a list.
 * ``{`` together with ``}`` creates an executable list/a procedure.
 * ``cvx`` converts a list to an executable list/procedure
 * ``cvlit`` converts an executable list/procedure back to a normal/litaral list
 * ``def`` assigns a value to a symbol.
 * ``exec`` executes the object on the stack.
 * ``mark`` puts a mark on the stack
 * ``counttomark`` counts the elements on the stack up to the topmost mark
 * ``cleartomark`` removes all objects from the stack up to the topmost mark but not the mark itself.

That's it. All the rest is done with extensions.


Execution
===============

The stack machine maintains a stack of dictionaries in which the values of the symbols are stored.
Every extention can register a dictionary with name/object pairs.
Callable objects are executable.
The machine tries to resolve the symbol by looking in each of the dictionaries in a top-down fashen.
If it finds a value, it executes the value.
*Execution* means:

 * If the object is callable, it is called.
 * If it is a symbol, the symbol is looked up and the process starts again recursively.
 * All other objects are put on the stack.


Examples
=========

List creation::

    [ 5.0 True "hello" ]

Executable list creation::

    { dup print }

This is syntactial sugar for::

    [ 'dup 'print ] cvx

Procedure definitaion::

    'average { 2 div } def
