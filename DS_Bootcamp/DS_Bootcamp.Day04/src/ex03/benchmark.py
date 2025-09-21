import timeit
import sys
from functools import reduce


def first_method(n):
    sum = 0
    for i in range(1, n+1):
        sum += i*i
    return sum

def second_method(n):
    return reduce(lambda sum, i: sum + i*i, range(1, n+1), 0)



def compare_time(func_name, num, n):
    func_names = {
        'loop': lambda: first_method(n),
        'reduce': lambda: second_method(n)
    }
    if func_name not in func_names:
        raise Exception("Available functions: loop, reduce")
    
    return timeit.timeit(func_names[func_name], number=num)

    

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: <name_of_function> <iterations> <number>")
        sys.exit(1)
    
    func_name = sys.argv[1]
    try:
        num = int(sys.argv[2])
        n = int(sys.argv[3])
    except ValueError as e:
        print("number of calls and number must be integer")
        sys.exit(1)

    try:
        execution_time = compare_time(func_name, num, n)
        print(execution_time)
    except Exception as e:
        print(e)
 