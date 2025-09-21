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

def third_method():
    return list(map(lambda email: email if '@gmail.com' in email else None, emails))


def compare_time():
    execution_time_1 = timeit.timeit(first_method, number=90_000)
    execution_time_2 = timeit.timeit(second_method, number=90_000)
    execution_time_3 = timeit.timeit(second_method, number=90_000)
    if (execution_time_1 < execution_time_2) and (execution_time_1 < execution_time_3):
        print('it is better to use a loop')
    elif (execution_time_2 < execution_time_1) and (execution_time_2 < execution_time_3):
        print('it is better to use a list comprehension')
    else:
        print('it is better to use a map')

    min_ex = min(execution_time_1, execution_time_2, execution_time_3)
    max_ex = max(execution_time_1, execution_time_2, execution_time_3)
    av_ex = execution_time_1 + execution_time_2 + execution_time_3 - (min_ex + max_ex)
    print (min_ex, 'vs', av_ex, 'vs', max_ex)

if __name__ == '__main__':
    compare_time()