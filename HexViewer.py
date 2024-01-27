

filename = input("Enter the file to open: ")
f = open (filename, 'rb')
bytes = 0 

line =[]

fileContents = f.read()
for b in fileContents:
    bytes = bytes + 1
    line.append(b)
    # print(b)
    print("{0:0{1}x}".format(b,2),end = " ")
    if bytes % 16 == 0:
        print("#", end="")
        for b2 in line:
            if(b2 >= 32) and (b2 <= 126):
                print(chr(b2),end="")
            else:
                print("*",end="")
        line = []
        print("")
        
print(" "*((3*(16-len(line)))-1), "#", end="")
for b2 in line:
    if(b2>=32) and (b2<=126):
        print(chr(b2), end="")
    else:
        print("*", end="")
f.close()