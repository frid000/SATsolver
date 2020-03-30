def main():
    graph = "g1"
    inputfilename = "graphs\\" + graph + ".txt"
    inputfile = open(inputfilename, "r")

    for line in inputfile:
        if line[0] == "c" or line[0] == "\n":  # comment or blank line
            continue
        elif line[0] == "p":  # problem line
            p_line = line.split(" ")
            nb_nodes = int(p_line[2])
            nb_edges = p_line[3]
            if "\n" in nb_edges:
                nb_edges = nb_edges.replace("\n", "")
            nb_edges = int(nb_edges)
            break
        else:
            print("Input file in not in the correct format.")

    edges = [[False for i in range(nb_nodes)] for j in range(nb_nodes)]

    actual_edges = 0

    for line in inputfile:
        if line[0] == "c" or line[0] == "\n":  # comment or blank line
            continue
        elif line[0] == "e":  # edge descriptors
            e_line = line.split(" ")
            u = int(e_line[1])
            v = e_line[2]
            if "\n" in v:
                v = v.replace("\n", "")
            v = int(v)
            edges[u-1][v-1] = True
            actual_edges += 1
        else:
            print("Input file is not in the correct format.")

    if nb_edges != actual_edges:
        print("The number of edges doesn't match the number of actual edges.")

    # Number of colours
    k = 20

    sat = ""
    nbvar = k * nb_nodes
    nbclauses = 0

    colouring = [[(i + (nb_nodes * j)) for j in range(k)] for i in range(1, nb_nodes + 1)]

    # each node has to have at least 1 colour
    for x in colouring:
        for y in x:
            sat += str(y) + " "
        sat += "0 \n"
        nbclauses += 1

    # each node can have at most 1 colour
    for i in range(nb_nodes):
        for j in range(k):
            for l in range(j + 1, k):
                sat += str(-colouring[i][j]) + " " + str(-colouring[i][l]) + " 0 \n"
                nbclauses += 1

    # every 2 nodes that share a common edge have to have different colours
    for i in range(nb_nodes):
        for j in range(nb_nodes):
            if edges[i][j]:
                for l in range(k):
                    sat += str(-colouring[i][l]) + " " + str(-colouring[j][l]) + " 0 \n"
                    nbclauses += 1

    first_line = "p cnf " + str(nbvar) + " " + str(nbclauses) + " \n"
    sat = first_line + sat

    outputfilename = "test_cases\\" + graph + "_" + str(k) + "-colouring.txt"
    outputfile = open(outputfilename, "w")
    outputfile.write(sat)
    outputfile.close()


if __name__ == "__main__":
    main()
