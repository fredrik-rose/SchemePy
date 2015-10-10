# SchemePy

SchemePy is a Scheme intepreter implemented in Python, inspired by the book
"Structure and Interpretation of Computer Programs" by Gerald Jay Sussman and
Hal Abelson.

# Installation

To install SchemePy, make sure you have Python 3.4 or greater installed. Then
run this command from the command prompt:

```
$ python setup.py install
```

If you're upgrading from a previous version, you need to remove it first.

# Usage

```
$ schemepy -h
usage: schemepy [-h] [--verbose]

optional arguments:
  -h, --help  show this help message and exit
  --verbose   increase output verbosity
```

## Example

```
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
```

# SchemePy language

SchemePy implements a subset of Scheme, with an extension: lazy evaluation. The
syntax for most parts of the language is identical to Scheme's syntax. SchemePy
supports tail-call optimizations.

## Basic types

### Boolean

```
#t
#f
```

### Integer number

```
4
```

### Floating point number

```
4.2
```

### Complex number

```
4+2i
```

### Symbol

```
'a
```

### String

```
"42"
```

### Pair

```
'(4 . 2)
```

### List

```
'(4 2)
```

## Expressions

### Self evaluating

```
> 4
4
```

### Quote

```
> 'a
a
```

### Definition

```
> (define a 4)
a
```

### Assignment

```
> (set! a 2)
a
```

### Identifier

```
> a
2
```

### If

```
> (if #t 4 2)
4
```

### Cond

```
> (cond (#f 4)
>       (#t 2)
>       (else 0))
2
```

### Lambda

```
> (lambda (a b) b)
#<compound procedure>
```

### Begin

```
> (begin
>     (define a 4)
>     a))
4
```

### Application

```
> (+ 4 2)
6
```

## Procedures

### Primitive

The following primitive procedures are supported:

`+`

```
> (+ 4 2)
6
```

`-`

```
> (- 4 2)
2
```

`*`

```
> (* 4 2)
8
```

`/`

```
> (/ 4 2)
2.0
```

`<`

```
> (< 4 2)
#f
```

`<=`

```
> (<= 4 2)
#f
```

`=`

```
> (= 4 2)
#f
```

`!=`

```
> (!= 4 2)
#t
```

`>=`

```
> (>= 4 2)
#t
```

`>`

```
> (> 4 2)
#t
```

`null?`

```
> (null? '())
#t
```

`cons`

```
> (cons 4 2)
(4 . 2)
```

`car`

```
> (car '(4 2))
4
```

`cdr`

```
> (cdr '(4 2))
(2)
```

`list`

```
> (list 4 2)
(4 2)
```

`append`

```
> (append '(4) '(2))
(4 2)
```

`display`

```
> (display 42)
42
```

`eval`

```
> (eval '(cons 4 2))
(4 . 2)
```

`apply`

```
> (apply cons '(4 2))
(4 . 2)
```

### Compound

An example of a compund procedure:

```
> (define (addOne n)
>     (+ n 1))
addOne
> (addOne 4)
5
```

## Lazy evaluation extension

It is possible to specify function parameter types:

Type                  | Syntax                         | Description
--------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------
Strict                | `(parameter s)` or `parameter` | The parameter is evaluated
Lazy                  | `(parameter l)`                | The evaluation of the parameter is delayed until needed
Lazy with memoization | `(parameter m)`                | The evaluation of the parameter is delayed until needed, the parameter is only evaluated once


### Examples

If parameter paramB is evaluated in the following example, we would get an
error (division by zero):

```
> (define (try paramA (paramB l))
>     (if (= 0 paramA)
>         1
>         paramB))
try
> (try 0 (/ 1 0))
1
```

Lazy evaluation enables us to create infinite lists:

```
> (define (cons (x l) (y l))
>     (lambda ((m l)) (m x y)))
cons
> (define (car (z l))
>     (z (lambda ((p l) (q l)) p)))
car
> (define (cdr (z l))
>     (z (lambda ((p l) (q l)) q)))
cdr
> (define (add-lists (list1 l) (list2 l))
>     (cons (+ (car list1) (car list2))
>           (add-lists (cdr list1) (cdr list2))
>     )
>  )
add-lists
> (define ones (cons 1 ones))
ones
> (define integers (cons 1 (add-lists ones integers)))
integers
> (car (cdr (cdr integers)))
3
```
