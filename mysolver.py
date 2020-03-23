import sys
import copy


def read_input(inputfilename):
    inputfile = open(inputfilename, "r")

    for line in inputfile:
        if line[0] == "p":
            p_line = line.split(" ")
            nbvar = int(p_line[2])
            nbclauses = int(p_line[3])
            break

    clauses = []
    for line in inputfile:
        if line[0] != "c":
            x = line.split(" ")
            if "\n" in x:
                x.remove("\n")
            if "0" in x:
                x.remove("0")
            if "0\n" in x:
                x.remove("0\n")
            clauses.append(x)

    return nbvar, nbclauses, clauses


def find_unit_clause(clauses):
    for cl in clauses:
        if len(cl) == 1:
            return cl[0]
    return None


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


def simplify(clauses, literal):
    i = 0
    while i < len(clauses):
        if literal in clauses[i]:
            clauses.remove(clauses[i])
            i = i - 1
        elif str(-int(literal)) in clauses[i]:
            clauses[i].remove(str(-int(literal)))
        i = i + 1
    return clauses


def DPLL(val, clauses):
    l1 = find_unit_clause(clauses)
    l2 = find_pure_literal(val, clauses)
    if l1 != None:
        literal = l1
    elif l2 != None:
        literal = l2
    else:
        literal = None

    while literal != None:
        clauses = simplify(clauses, literal)
        l = int(literal)
        val[abs(l) - 1] = l

        l1 = find_unit_clause(clauses)
        l2 = find_pure_literal(val, clauses)
        if l1 != None:
            literal = l1
        elif l2 != None:
            literal = l2
        else:
            literal = None

    if not clauses:
        return val

    for cl in clauses:
        if not cl:
            return None

    clauses1 = copy.deepcopy(clauses)
    literal = clauses[0][0]
    clauses.append([literal])
    sat = DPLL(val, clauses)
    if sat != None:
        return sat
    clauses = clauses[:-1]

    clauses = copy.deepcopy(clauses1)
    literal = str(-int(clauses[0][0]))
    clauses.append([literal])
    sat = DPLL(val, clauses)
    if sat != None:
        return sat
    clauses = clauses[:-1]

    return None


def main():
    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]

    nbvar, nbclauses, clauses = read_input(inputfilename)
    val = [None] * nbvar

    sat = DPLL(val, clauses)

    output = ""
    if sat == None:
        output = "0"
    else:
        for x in sat:
            if x != None:
                output += str(x)
                output += " "

    outputfile = open(outputfilename, "w")
    outputfile.write(output)
    outputfile.close()


if __name__ == "__main__":
    main()
