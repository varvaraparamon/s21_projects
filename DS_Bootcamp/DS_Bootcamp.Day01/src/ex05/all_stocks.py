import sys

def check_companies(string, COMPANIES, STOCKS):
    flag = 0
    if string in COMPANIES:
        print(string, 'stock price is', STOCKS[(COMPANIES[string])])
        flag = 1
    return flag

def check_stocks(string, COMPANIES, STOCKS):
    flag = 0
    keys = [key for key, value in COMPANIES.items() if value == string]
    if len(keys) == 1:
        print(string, 'is a ticker symbol for', keys[0])
        flag = 1
    return flag

def is_nothing(string, flag):
    if not flag:
        print(string, 'is an unknown company or an unknown ticker symbol')
        

def search():
    COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
    }

    STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90,
    'TSLA': 724.88,
    'NOK': 3.37
    }
    
    if (len(sys.argv) == 2):
        strings = sys.argv[1].split(',')
        strings = [string.replace(' ', '') for string in strings]
        if '' not in strings:
            for string in strings:
                flag = check_companies(string.capitalize(), COMPANIES, STOCKS)
                flag += check_stocks(string.upper(), COMPANIES, STOCKS)
                is_nothing(string, flag)

         

if __name__ == '__main__':
    search()