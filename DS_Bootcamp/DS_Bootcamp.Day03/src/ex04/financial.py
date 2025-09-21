import requests
from bs4 import BeautifulSoup
import sys
import time

def get_financial_data(ticker, field):
    url = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"URL does not exist or is not accessible: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    

    rows = soup.find_all('div', class_='row lv-0 yf-t22klz')
    if not rows:
        raise ValueError(f"Тикер '{ticker}' не найден или данные отсутствуют.")

    for row in rows:
        label = row.find('div', class_='rowTitle yf-t22klz')
        title = label.get('title')
        if title == field:
            nums = []
            columns = row.find_all('div', class_='column')
            for column in columns:
                nums.append(column.text.strip())
            return tuple(nums)
        
    raise Exception(f"Поле '{field}' не найдено")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python financial.py <ticker> <field>")
        sys.exit(1)


    ticker = sys.argv[1]
    field = sys.argv[2]

    try:
        data = get_financial_data(ticker, field)
        print(data)
    except Exception as e:
        print(e)
    except ValueError as e:
        print(e)

    time.sleep(5)

