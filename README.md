# SAT-Solver

solver.py takes 2 arguments: the Dimacs file containing the CNF and the file for the result.

/test_cases contains CNFs of different problems:
-Graph coloring (Actual graphs are in /graphs)
-N queens problem
-Sudoku
-One simple example from the lecture
-One unsatisfiable example

The generated solutions can be found in /solution

compareResults.py compares two solutions whether they contain the same variable assignments

run.bat runs the solver for each problem in /test_cases and writes the results into run.txt
