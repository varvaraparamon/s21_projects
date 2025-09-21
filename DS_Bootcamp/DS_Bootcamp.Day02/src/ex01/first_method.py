class Research:
    def file_reader(self):
        with open("data.csv", "r") as file:
            data = file.read()
        return data

if __name__ == '__main__':
    r = Research()
    print(r.file_reader())