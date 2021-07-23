import time

current_time = 0

def deco(function):
    pass





def speed_calc_decorator(function):
    def wrapper():
        print(function.__name__)
        current_time = time.time()
        function()
        end_time = time.time()
        print(f" this function took {end_time - current_time } time")
    return wrapper

@speed_calc_decorator
def fast_function():
    for i in range(10000000):
        i * i

@speed_calc_decorator
def slow_function():
    for i in range(100000000):
        i * i


fast_function()
slow_function()
# running_time = new_time - current_time
# print(running_time)