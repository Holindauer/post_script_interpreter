# Postscript Interpreter


This repository implements a minimal postscript interpreter with the ability to toggle between dynamic and lexical scoping.

# How to test

From the root dir run:

    $ pytest

# How to run

From the root dir run:

    $ python3 psip.py

This should start the repl:

    REPL>

# How to toggle scoping

### Dynamic Scoping

By default, scoping is dynamic and dictionaries are used to define new scopes:

    /x 1 def
    /func {
        3 dict begin
        /x 3 def 
        x
        end
    }def

    x func = =

Will output: 

    3
    1 

### Lexical Scoping

To switch to lexical scoping, use the **lexical** command:

    lexical 
    /x 9 def
	/f { x } def
    /y { /x 2 def f } def 
	/x 8 def
	y = 

Will output:

    9

This is because f captures a closure of x when defined. Then, even though x is refined both in the global and calling scope, x will still evaluate to 9 when evaluated inside the scope of f.

This style of lexical scoping does not utilize dictionaries, as is done in standard post script. Istead, this is how languages like python do scoping.

To switch back to dynamic scoping, use the **dynamic** command:

    dynamic
