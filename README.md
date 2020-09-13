# Magic Squares
A package containing algorithms for solving normal magic squares.

## Module: boards.py
The module has the class MSBoard. Apart from holding the data for its state, this contains the methods for solving itself with recursion and backtracking.
It is instanciated with one parameter, with the value of an integer >=3, for constructing a board for normal magic square of this order.

## Module: solvemsboard.py
The module can be run from the command line, as such:

`python solvemsboard.py <order:int> <limit:int>`

It will create magic squares randomly from any order equal or greater than 3 (orders beyond 6 takes a lot of time). The limit is optional, if missing the program will generate all possible squares. 

### Example square of 7x7 order
A magic square of 7th order, discoverd by the algorithms in this package.

```
175
     | 16 | 36 |  4 | 41 |  2 | 48 | 28 | 175
     |----|----|----|----|----|----|----|
     | 17 | 40 | 43 | 20 | 18 | 23 | 14 | 175
     |----|----|----|----|----|----|----|
     | 15 | 22 | 31 | 32 | 46 |  3 | 26 | 175
     |----|----|----|----|----|----|----|
     | 27 |  7 |  6 | 30 | 42 | 39 | 24 | 175
     |----|----|----|----|----|----|----|
     | 45 | 38 | 29 | 33 | 13 | 12 |  5 | 175
     |----|----|----|----|----|----|----|
     | 47 | 11 | 37 | 10 | 35 |  1 | 34 | 175
     |----|----|----|----|----|----|----|
     |  8 | 21 | 25 |  9 | 19 | 49 | 44 | 175
     |----|----|----|----|----|----|----|
175   175  175  175  175  175  175  175
```