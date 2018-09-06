""" This is a collection of python data structures """


simple_list = [1,2,3,4]
simple_list.extend([5,6,7])

del(simple_list[0])

# creating a simple dictionary
my_dictionary = {'name': 'michael'}
print(my_dictionary.items())

# iteration on a dictionary
for key, val in my_dictionary.items():
    print("THis is output ", key,val)


