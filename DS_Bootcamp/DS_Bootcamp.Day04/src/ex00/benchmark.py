import timeit


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


def compare_time():
    execution_time_1 = timeit.timeit(first_method, number=90_000)
    execution_time_2 = timeit.timeit(second_method, number=90_000)
    print ('it is better to use a list comprehension' if execution_time_2 < execution_time_1 else 'it is better to use a loop')
    print (min(execution_time_1, execution_time_2), 'vs', max(execution_time_1, execution_time_2))

if __name__ == '__main__':
    compare_time()