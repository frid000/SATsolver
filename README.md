# SAT-Solver

mysolver.py takes 2 arguments: the Dimacs file containing the CNF and the file for the result.
Because we choose random literals during the algorithm, runs can differ in execution time.
For our example g3_11-colouring.txt, the algorithm took in ten runs on average 11.8 seconds and runtime ranged between 10.4 and 14.5 seconds.

Our example problem contains 1.375 variables and 15.096 clauses.

/test_cases contains CNFs of different problems:
* Graph coloring (Actual graphs are in /graphs)
* N queens problem
* Sudoku
* One simple example from the lecture
* One unsatisfiable example

The generated solutions can be found in /solution

/util contains different scripts:
* compareResults.py compares two solutions whether they contain the same variable assignments
* run.bat runs the solver for each problem in /test_cases and writes the results into run.txt
* generate_k-colouring_sat.py which creates CNF formulas for graph coloring
* generate_nqueens_sat.py which creates CNF formulas for the n queens problem

# Run the program

python mysolver.py g3_11-colouring.txt result.txt

# Possible further improvements

The following slides provide further ideas to improve the performance. One which could be implemented with limited effort is the restart of the search after some decisions.
https://baldur.iti.kit.edu/sat/files/2016/l05.pdf


# Authors

Jan Fekonja
Florentin Wieser