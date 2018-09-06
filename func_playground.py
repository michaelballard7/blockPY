""" unpacking function arguments with * for a list or tuple """
# use the single star on unNamed arguements
def unlimited_arguements(*args):
    print(args) # will return a tuple
    for argument in args: 
        print(argument)

unlimited_arguements(1,2,3,4)
unlimited_arguements(*[1,2,3,4])


""" Unpacking function arguements with ** for a dictionary """ 
# use the ** on name arguments
def unlimited_args(**keyword_args):
    print(keyword_args)

    for k, arg in keyword_args.items():
        print(k, arg)

unlimited_args(name="Michael", age=28)