import sys

def value_search():
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
        ticker = sys.argv[1].upper()
        keys = [key for key, value in COMPANIES.items() if value == ticker]
        if len(keys) == 1:
            print(keys[0], STOCKS[ticker])
        else:
            print("Unknown company")


if __name__ == '__main__':
    value_search()