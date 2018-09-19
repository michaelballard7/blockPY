
# Working with files in python

""" To Write content to a file """
# f = open('demo.txt', mode='w') 
# f.write('Add this content')
# f.close()

""" To Read content to a file """
# f = open('demo.txt', mode='r') 
# file_content = f.read() # returns content on one line as a string

# file_content = f.readlines() #returns the list of lines as strings  
# for line in file_content:
#     print(line[-1]) #select every element in the line with the exception of the line break char

# line = f.readline() 
# while line:
#     print(line)
#     line = f.readline()
# f.close()


""" To Append content to a file """
# f = open('demo.txt', mode='a') 
# f.write(" + Append this content \n")
# f.close()

""" Manage file with the with keyword to auto open and close file """

with open('demo.txt', mode='r') as f:

    line = f.readline()

    while line:
        print(line)
        line = f.readline()

print("Done")
