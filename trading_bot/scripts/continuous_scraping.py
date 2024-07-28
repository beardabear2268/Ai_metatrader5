import MetaTrader5 as mt5
import pandas as pd
import logging
import time
from datetime import datetime
from pattern_recognition import recognize_patterns
from trading_strategies import implement_strategy

def initialize_mt5(account, password, server):
    if not mt5.initialize():
        logging.error("Initialize() failed, error code =", mt5.last_error())
        quit()

    authorized = mt5.login(account=account, password=password, server=server)
    if authorized:
        logging.info("Connected to account #{}".format(account))
    else:
        logging.error("Failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

def shutdown_mt5():
    mt5.shutdown()

def fetch_realtime_data(symbol):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 1)
    if rates is None:
        logging.error("Failed to fetch rates for {}".format(symbol))
        return None

    rates_frame = pd.DataFrame(rates)
    return rates_frame

def append_to_csv(df, file_path):
    df.to_csv(file_path, mode='a', header=not pd.io.common.file_exists(file_path), index=False)

def scrape_and_add_data(symbol, data_path, duration_minutes=120):
    start_time = datetime.now()
    end_time = start_time + pd.to_timedelta(duration_minutes, unit='m')

    while datetime.now() < end_time:
        df = fetch_realtime_data(symbol)
        if df is not None and not df.empty:
            df = recognize_patterns(df)
            df = implement_strategy(df, strategy='ma')  # Example: Moving Average strategy
            append_to_csv(df, data_path)
            logging.info(f"Data appended to {data_path}")

        time.sleep(60)  # Wait for 1 minute

if __name__ == "__main__":
    logging.basicConfig(filename='../logs/continuous_scraping.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    