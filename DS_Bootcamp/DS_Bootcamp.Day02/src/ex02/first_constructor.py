import sys

class Research:
    def __init__(self, filname):
        self.filename = filname

    def file_reader(self):
        data = []
        data_str = ''
        with open(self.filename, "r") as file:
            for line in file:
                data.append(line)
                data_str += line
        self.check_data(data)
        return data_str
    
    def check_data(self, data):
        if len(data[0].split(',')) != 2:
            print(data[0].split(','))
            raise Exception("Wrong data head")
        for line in data[1:]:
            if (line.replace('\n', '') != '0,1') and (line.replace('\n', '') != '1,0'):
                raise Exception("Wrong data tail")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 first_constructor.py <filename>")
        sys.exit(1)
        
    try:
        r = Research(sys.argv[1])
        print(r.file_reader())
    except Exception as e:
        print(f"Error: {e}")


