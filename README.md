# SchemePy

SchemePy is a Scheme intepreter implemented in Python, inspired by the book
"Structure and Interpretation of Computer Programs" by Gerald Jay Sussman and
Hal Abelson.

# Installation

To install SchemePy, make sure you have Python 3.4 or greater installed. Then
run this command from the command prompt:

    python setup.py install

If you're upgrading from a previous version, you need to remove it first.

# Usage

When SchemePy has been install, run this command from the command prompt:

    schemepy

You should now see:

    Welcome to SchemePy!
    >

Now you can start typing Scheme expressions!

## Example
    $ schemepy
    Welcome to SchemePy!
    > (define (factorial n)
    >     (if (= n 1)
    >         n
    >         (* n (factorial (- n 1)))
    >     )
    > )
    factorial
    > (factorial 10)
    3628800
    >
