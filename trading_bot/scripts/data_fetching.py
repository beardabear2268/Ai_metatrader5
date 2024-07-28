import pandas as pd
import numpy as np
import logging
import requests
import concurrent.futures

def fetch_ohlcv_data(symbol, interval):
    try:
        url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}'
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                         'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                         'taker_buy_quote_asset_volume', 'ignore'])

        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        if not validate_data(df):
            logging.warning(f"Data validation failed for symbol: {symbol}")
            return pd.DataFrame()

        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred while fetching data for {symbol}: {http_err}")
    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
    return pd.DataFrame()

def validate_data(df):
    required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    for column in required_columns:
        if column not in df.columns:
            logging.warning(f"Missing required column: {column}")
            return False
    return True

def fetch_ohlcv_data_concurrently(symbols, interval):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(fetch_ohlcv_data, symbol, interval) for symbol in symbols]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            valid_results = [result for result in results if not result.empty]

        if not valid_results:
            logging.error("No valid data frames were fetched.")
            return pd.DataFrame()

        combined_df = pd.concat(valid_results, ignore_index=True)
        return combined_df
    except Exception as e:
        logging.error(f"Failure in concurrent data fetching: {e}")
        return pd.DataFrame()