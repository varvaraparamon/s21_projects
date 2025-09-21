import timeit
import random
from collections import Counter

rand_list = [random.randint(0, 100) for i in range(1_000_000)]

def func():
    dct = {i: 0 for i in range(101)}
    for elem in rand_list:
        dct[elem] += 1
    return dct

def func_counter():
    return Counter(rand_list)

def top():
    dct = func()
    return sorted(dct.items(), key = lambda x: x[1], reverse = True)[:10]

def top_counter():
    return Counter(rand_list).most_common(10)


if __name__ == '__main__':
    print(f"my function: {timeit.timeit(func, number=1)}")
    print(f"Counter: {timeit.timeit(func_counter, number=1)}")
    print(f"my top: {timeit.timeit(top, number=1)}")
    print(f"Counter's top: {timeit.timeit(top_counter, number=1)}")