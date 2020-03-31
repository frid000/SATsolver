def nqueens_sat(n):
    chess = [[(x + (n * y)) for x in range(1, n+1)] for y in range(n)]
    nbvar = n * n
    nbclauses = 0
    sat = ""

    # at least one queen in each row
    for i in range(n):
        for j in range(n):
            sat = sat + str(chess[i][j]) + " "
        sat = sat + "0 \n"
        nbclauses += 1

    # at most one queen in each row and at most one queen in each column
    for k in range(n):
        for i in range(n):
            for j in range(i+1, n):
                sat = sat + str(-chess[k][i]) + " " + str(-chess[k][j]) + " 0 \n"
                sat = sat + str(-chess[i][k]) + " " + str(-chess[j][k]) + " 0 \n"
                nbclauses += 2

    # at most one queen at each diagonal
    for i in range(n):
        for j in range(n):
            for k in range(i+1, n):
                for l in range(n):
                    if (i+j == k+l) or (i-j == k-l):
                        sat = sat + str(-chess[i][j]) + " " + str(-chess[k][l]) + " 0 \n"
                        nbclauses += 1

    first_line = "p cnf " + str(nbvar) + " " + str(nbclauses) + "\n"
    sat = first_line + sat

    return sat


def main():
    # n has to be al least 4 (otherwise it doesn't make sense)
    n = 23
    cnf = nqueens_sat(n)

    filename = "test_cases\\queens_" + str(n) + ".txt"
    file = open(filename, "w")
    file.write(cnf)
    file.close()


if __name__ == "__main__":
    main()
