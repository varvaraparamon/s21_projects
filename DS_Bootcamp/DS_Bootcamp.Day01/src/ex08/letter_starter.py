import sys

def letter_starter():
    if len(sys.argv) == 2:
        f_read = open('employees.tsv', 'r')

        name = ''
        for line in f_read:
            lines = line.split('\t')
            if lines[2] == sys.argv[1] + '\n':
                name = lines[0]
        
        if name:
            print(f"""Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. 
That’s a precondition for the professionals that our company hires.""")
        else:
            print('no such email in db')
    
if __name__ == '__main__':
    letter_starter()