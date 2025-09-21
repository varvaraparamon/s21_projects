import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ex03')))

from financial import get_financial_data

def test_total_revenue():
    ticker = 'MSFT'
    field = 'Total Revenue'
    data = get_financial_data(ticker, field)
    assert isinstance(data, tuple), "The return type should be a tuple"
    assert data[0] == 'Total Revenue', "The first element should be 'Total Revenue'"
    assert all(isinstance(item, str) for item in data), "All elements should be strings"

def test_invalid_ticker():
    ticker = 'INVALID_TICKER'
    field = 'Total Revenue'
    with pytest.raises(Exception):
        get_financial_data(ticker, field)

def test_invalid_field():
    ticker = 'MSFT'
    field = 'Invalid Field'
    with pytest.raises(Exception):
        get_financial_data(ticker, field)

def test_type_return():
    ticker = 'MSFT'
    field = 'Total Revenue'
    data = get_financial_data(ticker, field)
    assert isinstance(data, tuple), "The return type should be a tuple"

if __name__ == "__main__":
    pytest.main()