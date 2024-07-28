import requests
import logging

def fetch_symbols():
    try:
        url = 'https://api.binance.com/api/v3/exchangeInfo'
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        symbols = [symbol_info['symbol'] for symbol_info in data['symbols'] if symbol_info['status'] == 'TRADING']
        
        logging.info("Fetched symbols: %s", symbols)
        return symbols
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred while fetching symbols: {http_err}")
    except Exception as e:
        logging.error(f"Error fetching symbols: {e}")
        return []
