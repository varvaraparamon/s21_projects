import sys

class Research:
    def __init__(self, filname):
        self.filename = filname

    def file_reader(self, has_header = True):
        data = []
        with open(self.filename, "r") as file:
            for line in file:
                data.append(line.strip().split(','))

        if has_header:
            if len(data[0]) != 2:
                raise Exception("Wrong data head")
            data = [list(map(int, line)) for line in data[1:]]
        else:
            data = [list(map(int, line)) for line in data]
        self.check_data(data)
        return data
    
    def check_data(self, data):
        for line in data:
            if (line != [1, 0]) and (line != [0, 1]):
                raise Exception("Wrong data tail")
            
    class Calculations:
        def counts(data):
            heads = sum(line[0] for line in data)
            tails = sum(line[1] for line in data)
            return heads, tails

        def fractions(heads, tails):
            all = heads + tails
            return 100*heads/all, 100*tails/all
                

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 first_nest.py <filename>")
        sys.exit(1)

    try:
        r = Research(sys.argv[1])
        data = r.file_reader(True)
        print(data)

        heads, tails = r.Calculations.counts(data)
        print(heads, tails)

        heads_perc, tails_perc = r.Calculations.fractions(heads, tails)
        print(heads_perc, tails_perc)

    except Exception as e:
        print(f"Error: {e}")


