import sys

def main():

	inputfile1 = open(sys.argv[1], "r")  # open input file
	inputfile2 = open(sys.argv[2], "r")  # open input file
	
	list1 = []
	list2 = []
	
	
	for line in inputfile1:
		x = line.split(" ")
		list1 = x
		
	for line in inputfile2:
		x = line.split(" ")
		list2 = x
	
	if len(list1) != len(list2):
		print("Files differ in length!")
		return
	
	list1.sort()
	list2.sort()
	
	for i in range(0,len(list1)):
		if list1[i] != list2[i]:
			print("Files contain unequal assignments!")
			return
	
	print("Files are equal")
		






if __name__ == "__main__":
    main()
