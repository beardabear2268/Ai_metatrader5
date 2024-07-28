import MetaTrader5 as mt5
import pandas as pd
import logging
import time
from datetime import datetime
from pattern_recognition import recognize_patterns

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

def fetch_realtime_data(symbol, num_candles=1000):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, num_candles)
    if rates is None:
        logging.error("Failed to fetch rates for {}".format(symbol))
        return None

    rates_frame = pd.DataFrame(rates)
    return rates_frame

def main():
    logging.basicConfig(filename='../logs/generate_training_data.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    
    account = 12345678 
    password = "your_password"
    server = "broker_server"

    initialize_mt5(account, password, server)
    
    symbol = "CADBTC"
    data_path = f'../data/{symbol}_training_data.csv'
    df = fetch_realtime_data(symbol)

    if df is not None and not df.empty:
        df = recognize_patterns(df)
        df.to_csv(data_path, index=False)
        logging.info(f"Data saved to {data_path}")
    
    shutdown_mt5()

if __name__ == "__main__":
    main()