import timeit
import sys


emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']

def first_method():
    gmail_emails = []
    for email in emails:
        if '@gmail.com' in email:
            gmail_emails.append(email)
    return gmail_emails

def second_method():
    return [email for email in emails if '@gmail.com' in email]

def third_method():
    return list(map(lambda email: '@gmail.com' in email, emails))

def fourth_method():
    return list(filter(lambda email: '@gmail.com' in email, emails))


def compare_time(func_name, num):
    func_names = {
        'loop': first_method,
        'list_comprehension': second_method, 
        'map': third_method,
        'filter': fourth_method
    }
    if func_name not in func_names:
        raise Exception("Available functions: loop, list_comprehension, map, filter")
    
    return timeit.timeit(func_names[func_name], number=num)

    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: <name_of_function> <iterations>")
        sys.exit(1)
    
    func_name = sys.argv[1]
    try:
        num = int(sys.argv[2])
    except ValueError as e:
        print("number of calls must be integer")
        sys.exit(1)

    try:
        execution_time = compare_time(func_name, num)
        print(execution_time)
    except Exception as e:
        print(e)
