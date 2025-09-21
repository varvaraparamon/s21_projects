def name_extract():
    f_read = open('emails.txt', 'r')
    f_write = open('employees.tsv', 'w')

    f_write.write('Name' + '\t' + 'Surname' + '\t' + 'E-mail\n')
    for line in f_read:
        names = line.split('@')[0].split('.')
        names = [name.capitalize() for name in names]
        f_write.write(names[0] + '\t' + names[1] + '\t' + line)

if __name__ == '__main__':
    name_extract()