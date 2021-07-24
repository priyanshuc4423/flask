def loggin(function):
    def wrapper(*args,**kwargs):
        function(args[0])
        print(function.__name__)
        print(args[0])

    return wrapper

@loggin
def hello_world(name):
     print(f"HellO {name} ")

@loggin
def byeworld(cause):
    print(f"You died  due to {cause}")

hello_world("aditi")
byeworld("jumpofbuilding")
