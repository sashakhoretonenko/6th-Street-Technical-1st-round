import os
import requests
import sys
from datetime import datetime, timedelta

class StockClient:
#---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
        if not self.API_KEY:
            raise ValueError("Missing Alpha Vantage API Key.")
        
        self.base_url = "https://www.alphavantage.co/query"
#---------------------------------------------------------------------------------------------------------------------------------------
    def check_api(self):
        if not self.API_KEY:
            raise ValueError("Missing Alpha Vantage API Key.")
#---------------------------------------------------------------------------------------------------------------------------------------
    def make_request(self, params):
        try:
            response = requests.get(self.base_url, params)
            return response
        except Exception as e:
            raise ValueError(f"Error during request: {e}")
        
#---------------------------------------------------------------------------------------------------------------------------------------
    
    # given a symbol and a date, return the open, high, low, close, and volume for that symbol on that date.
    def lookup(self, symbol: str, date: str):
        # Check to see if we need to use compact and that date is in correct format
        try:
            requested_date = datetime.strptime(date, '%Y-%m-%d')
            current_date = datetime.now()
            cutoff_date = current_date - timedelta(days=100)
            outputsize = 'compact'
            if requested_date < cutoff_date:
                outputsize = 'full'
        except ValueError:
            raise ValueError("Date format should be YYYY-MM-DD.")

        # Fetch data
        params = {
            'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'apikey': self.API_KEY,
                'outputsize': outputsize
        }
        response = self.make_request(params)
        data = response.json()

        time_series = time_series = data['Time Series (Daily)']
        
        # Check that the date is within the time_series
        if date not in time_series:
            raise ValueError("Date is invalid or information regarding the date is not available.")
        
        final_data = time_series[date]

        # Example format
        # "Time Series (Daily)": {
        #     "2025-04-01": {
        #         "1. open": "248.0300",
        #         "2. high": "250.6200",
        #         "3. low": "243.4900",
        #         "4. close": "250.3400",
        #         "5. volume": "4413139"
        #     }

        return {
            'open': float(final_data['1. open']),
            'high': float(final_data['2. high']),
            'low': float(final_data['3. low']),
            'close': float(final_data['4. close']),
            'volume': int(final_data['5. volume'])
        }

    #---------------------------------------------------------------------------------------------------------------------------------------

    # given a symbol and a range 'n', return the lowest price that symbol traded at over the last 'n' data points (lowest low).
    def min(self, symbol: str, n: int):
        self.check_api()

        # Check whether we can just use compact data or not
        outputsize = 'compact'
        if n > 100:
            outputsize = 'full'

        # Fetch data
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.API_KEY, 
            'outputsize': outputsize
        }

        # Get data
        response = self.make_request(params)
        data = response.json()
        time_series = data['Time Series (Daily)']

        # Sort dates in descending order and consider only first n
        dates = sorted(time_series.keys(), reverse=True)
        dates = dates[:n]

        min_low_price = float('inf')

        for date in dates:
            low = float(time_series[date]['3. low'])
            min_low_price = min(min_low_price, low)
        
        return min_low_price
    
#---------------------------------------------------------------------------------------------------------------------------------------
    # given a symbol and a range 'n', return the highest price that symbol traded at over the last 'n' data points (highest high).
    def max(self, symbol: str, n: int):
        self.check_api()

        # Check whether we can just use compact data or not
        outputsize = 'compact'
        if n > 100:
            outputsize = 'full'

        # Fetch data
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.API_KEY, 
            'outputsize': outputsize
        }

        # Get data
        response = self.make_request(params)
        data = response.json()
        time_series = data['Time Series (Daily)']

        # Sort dates in ascending order and consider only first n
        dates = sorted(time_series.keys(), reverse=True)
        dates = dates[:n]

        max_high_price = float('-inf')

        for date in dates:
            high = float(time_series[date]['2. high'])
            max_high_price = max(max_high_price, high)

        return max_high_price
        