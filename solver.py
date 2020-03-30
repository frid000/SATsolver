import sys
import time
import collections
import random


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
            if "" in x:
                x.remove("")
            clauses.append(list(map(int, x)))  # list of lists of integers

    if len(clauses) != nbclauses:
        print("The number of clauses doesn't match the number of actual clauses.")
    
    return nbvar, nbclauses, clauses  # return number of variables, number of clauses and actual clauses


# Find all unit clauses or return None if unit clauses doesn't exists
# Unit clauses is a clause that exists of a single literal
# returns the variables of the unit clauses
def find_unit_clauses(clauses):
    unit_clauses = []
    for cl in clauses:
        if len(cl) == 1:
            unit_clauses.append(cl[0])
    return list(dict.fromkeys(unit_clauses)) #remove duplicates


# clauses is a list of list: [[3,-1],[1,2],[-1,2,-3]]

# Find all pure literals
# A pure literal is a literal that occurs either only unnegated or only negated within the whole CNF
# returns all pure literals
def find_pure_literals(clauses):
    positive = set()
    negative = set()
    result = []
    for clause in clauses:
        for x in clause:
            if x < 0:
                negative.add(-x)
            else:
                positive.add(x)
    # get all variables that either occur positive or negative
    pures = negative.symmetric_difference(positive)

    for p in pures.intersection(negative):
        result.append(-p)
    for p in pures.intersection(positive):
        result.append(p)

    return result


#Simplify clauses by literal l means to do the following:
#- drop all clauses containing literal l in the same orientation
#- retain all other clauses but omit all literals (not l)
def simplify(clauses, literal):
    i = 0
    while i < len(clauses):
        if literal in clauses[i]:  # drop all clauses containing the literal in the same orientation
            clauses.remove(clauses[i])
            i = i - 1  # necessary as one clause is removed
        elif -literal in clauses[i]:  # retain other clauses but omit negated literal from them
            clauses[i].remove(-literal)
        i = i + 1
        
    return clauses


# select the next literal
def select_literal(clauses):
    #return clauses[0][0]
    return random.choice(random.choice(clauses))



# DPLL algorithm from the lectures
def DPLL(val, clauses):

    #print("clauses: ", clauses)
    #print("valuation: ", val)

    # find all unit clauses and simplify CNF
    unit_clauses = find_unit_clauses(clauses)
    #print('found unit clauses: ', unit_clauses)
    for unit in unit_clauses:
        clauses = simplify(clauses, unit)
        val.append(unit)

    #Either do unit_clause-simplification OR literal-simplification
    if len(unit_clauses) == 0:
        # find pure literals and simplify CNF
        pure_literals = find_pure_literals(clauses)
        #print('found pure literalts: ', pure_literals)
        for pure in pure_literals:
            clauses = simplify(clauses, pure)
            val.append(pure)

    #print("simplyfied clauses: ", clauses)

    ## Goaltest
    
    # empty conjunction is True -> the problem is satisfiable and we are done
    if not clauses: 
        return val  # Return satisfiable valuation

    # empty clause (disjunction of nothing) is False -> fail
    for cl in clauses:
        if not cl:
            return None
    
    # choose a literal from the CNF (first one)
    literal = select_literal(clauses)

    # Performance issue -> replace deepcopy with [list(x) for x in clauses]
    next_clauses_1 = [list(x) for x in clauses]
    next_clauses_2 = [list(x) for x in clauses]
    next_val_1 = val.copy()
    next_val_2 = val.copy()

    next_clauses_1.append([literal])
    next_clauses_2.append([-literal])

    res1 = DPLL(next_val_1, next_clauses_1)
    if res1 is not None: # found solution
        return res1
    else: #didnt find solution
        return DPLL(next_val_2, next_clauses_2)


#Checks if the solution holds
def check_solution(val, clauses):
    for cl in clauses:
        found = False
        for x in cl:
            if x in val:
                found = True
                break; #break for-loop for current clause
        if not found:
            return False
    return True


def main():
    inputfilename = sys.argv[1]  # get name of the input file
    outputfilename = sys.argv[2]  # get name of the output file

    nbvar, nbclauses, clauses = read_input(inputfilename)  # read input file
    val = []# valuation is a list of all assigned values
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
