import sys

clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
'elon@paypal.com', 'jessica@gmail.com']

participants = ['walter@heisenberg.com', 'vasily@mail.ru',
'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']

recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

def call_center():
    call_center_set = set(clients) - set(recipients)
    print(list(call_center_set))

def potential_clients():
    potential_clients_set = set(participants) - set(clients)
    print(list(potential_clients_set))

def loyalty_program():
    loyalty_program_set = set(clients) - set(participants)
    print(list(loyalty_program_set))

def buisness_task():
    names_list = ['call_center', 'potential_clients', 'loyalty_program']
    if (len(sys.argv) == 2):
        if sys.argv[1] == names_list[0]:
            call_center()
        elif sys.argv[1] == names_list[1]:
            potential_clients()
        elif sys.argv[1] == names_list[2]:
            loyalty_program()
        else:
            raise NameError('error in argument name')

if __name__ == '__main__':
    try:
        buisness_task()
    except NameError as err:
        print(err)