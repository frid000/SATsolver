import sys
import copy
import time
import collections


# Read input from a file in Dimacs format specifying a cnf formula
def read_input(inputfilename):
    inputfile = open(inputfilename, "r")  # open input file
    clauses = []

    for line in inputfile:
        if line[0] == "p":  # information about the problem
            p_line = line.split(" ")
            if p_line[1] != "cnf":
                print("Odd file format. Should be in Dimacs format with \'cnf\' in problem line.")
            nbvar = int(p_line[2])  # get number of variables
            nbclauses = int(p_line[3])  # get number of clauses
        elif line[0] == "c" or line[0] == "\n":  # comment or blank line
            continue
        else:  # actual clauses
            x = line.split(" ")
            if "\n" in x:
                x.remove("\n")
            if "0" in x:
                x.remove("0")
            if "0\n" in x:
                x.remove("0\n")
            clauses.append(x)  # list of lists

    if len(clauses) != nbclauses:
        print("The number of clauses doesn't match the number of actual clauses.")

    return nbvar, nbclauses, clauses  # return number of variables, number of clauses and actual clauses


# Find first unit clause or return None if unit clauses doesn't exists
# Unit clauses is a clause that exists of a single literal
def find_unit_clause(clauses):
    for cl in clauses:
        if len(cl) == 1:
            return cl[0]
    return None


# Find pure literal or return None if pure literal doesn't exists
# A pure literal is a literal that occurs either only unnegated or only negated within the whole CNF
def find_pure_literal(val, clauses):
    for i in range(1, len(val) + 1):
        occurs_pos = False
        occurs_neg = False
        for cl in clauses:
            if str(i) in cl:
                occurs_pos = True
            if str(-i) in cl:
                occurs_neg = True
        if occurs_pos and (not occurs_neg):
            return str(i)
        elif (not occurs_pos) and occurs_neg:
            return str(-i)
    return None


"""
Simplify clauses by literal l means to do the following:
- drop all clauses containing literal l in the same orientation
- retain all other clauses but omit all literals (not l)
"""


def simplify(clauses, literal):
    i = 0
    while i < len(clauses):
        if literal in clauses[i]:  # drop all clauses containing the literal in the same orientation
            clauses.remove(clauses[i])
            i = i - 1  # necessary as one clause is removed
        elif str(-int(literal)) in clauses[i]:  # retain other clauses but omit negated literal from them
            clauses[i].remove(str(-int(literal)))
        i = i + 1
    return clauses


# Find the variable that occurs the most (DON'T distinguish between negative and positive literals)
def find_most_common(clauses):
    to_list = []
    for cl in clauses:
        for l in cl:
            to_list.append(abs(int(l)))
    most_common = collections.Counter(to_list).most_common(1)[0][0]
    return str(most_common)


# Find the variable that occurs the most (DO distinguish between negative and positive literals)
def find_most_common_distinguish(clauses):
    to_list = []
    for cl in clauses:
        for l in cl:
            to_list.append(int(l))
    most_common = collections.Counter(to_list).most_common(1)[0][0]
    return str(most_common)


# DPLL algorithm from the lectures
def DPLL(val, clauses):
    l1 = find_unit_clause(clauses)  # find a unit clause
    l2 = find_pure_literal(val, clauses)  # find a pure literal
    if l1 is not None:
        literal = l1
    elif l2 is not None:
        literal = l2
    else:
        literal = None

    while literal is not None:  # simplify cnf unit there are no more unit clauses or pure literals
        clauses = simplify(clauses, literal)
        l = int(literal)
        val[abs(l) - 1] = l  # valuation of literals
        # If l > 0 then l is a positive literal; if l < 0 then l is a negative literal

        l1 = find_unit_clause(clauses)
        l2 = find_pure_literal(val, clauses)
        if l1 is not None:
            literal = l1
        elif l2 is not None:
            literal = l2
        else:
            literal = None

    if not clauses:  # empty conjunction is True -> the problem is satisfiable and we are done
        return val  # Return satisfiable valuation

    for cl in clauses:
        if not cl:  # empty clause (disjunction of nothing) is False -> fail
            return None

    clauses1 = copy.deepcopy(clauses)
    literal1 = clauses[0][0]  # use the first literal in the first clause
    # literal1 = find_most_common(clauses)
    # literal1 = find_most_common_distinguish(clauses)
    clauses.insert(0, [literal1])
    sat = DPLL(val, clauses)  # Recursive call
    if sat is not None:
        return sat  # Return solution if found

    clauses = copy.deepcopy(clauses1)
    literal1 = str(-int(literal1))  # opposite value than before
    clauses.insert(0, [literal1])
    sat = DPLL(val, clauses)  # Recursive call
    if sat is not None:
        return sat  # Return solution if found

    return None  # Fail because we can't find solution if one literal can't be True and can't be False (not satisfiable)


def check_solution(val, clauses):
    for cl in clauses:
        at_least_one_true = False
        for x in cl:
            if val[abs(int(x)) - 1] is None:
                val[abs(int(x)) - 1] = 0
            elif int(x) > 0 and val[abs(int(x)) - 1] > 0:
                at_least_one_true = True
                break
            elif int(x) < 0 and val[abs(int(x)) - 1] < 0:
                at_least_one_true = True
                break
        if not at_least_one_true:
            return False
    return True


def main():
    inputfilename = sys.argv[1]  # get name of the input file
    outputfilename = sys.argv[2]  # get name of the output file

    nbvar, nbclauses, clauses = read_input(inputfilename)  # read input file
    val = [None] * nbvar  # valuation is a list of size nbvar (number of variables)
    original_clauses = copy.deepcopy(clauses)

    start_time = time.time()

    sat = DPLL(val, clauses)
    # DPLL algorithm returns satisfiable valuation of the literals if the problem is satisfiable
    # or it returns None if the problem is not satisfiable

    end_time = time.time()
    time_needed = end_time - start_time
    print("The DPLL algorithm took " + str(time_needed) + " seconds to finish.")

    output = ""
    if sat is None:  # solution not found
        output = "0"  # output file contains single entry 0
    else:  # solution found
        for x in sat:
            if x is not None:  # not assigning truth values to variables that can be either True or False
                output += str(x)
                output += " "

    outputfile = open(outputfilename, "w")  # overwrite any existing content in the output file
    outputfile.write(output)  # write to the output file
    outputfile.close()

    if sat is None:
        print("Not satisfiable.")
    elif check_solution(sat, original_clauses):
        print("Solution is found and it holds.")
    else:
        print("Something went wrong.")


if __name__ == "__main__":
    main()
