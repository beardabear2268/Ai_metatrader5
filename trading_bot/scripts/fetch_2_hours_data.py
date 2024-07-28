import MetaTrader5 as mt5
import pandas as pd
import logging
import time
from datetime import datetime

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

def run_streaming_data(symbol, output_path, duration_minutes=120):
    data = []
    start_time = datetime.now()
    end_time = start_time + pd.to_timedelta(duration_minutes, unit='m')

    while datetime.now() < end_time:
        rates_frame = fetch_realtime_data(symbol)
        if rates_frame is not None and not rates_frame.empty:
            data.append(rates_frame)
            logging.info(f"Fetched data: {rates_frame.to_dict()}")

        time.sleep(60)  # Wait for the next minute

    if data:
        df = pd.concat(data)
        df.to_csv(output_path, index=False)
        logging.info(f"Data saved to {output_path}")
    else:
        logging.error("No data collected during the period.")

if __name__ == "__main__":
    logging.basicConfig(filename='../logs/fetch_2_hours_data.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    
    # Replace with your account details
    account = 7052173
    password = "Hilary2268!"
    server = "FPMarketsLLC-Demo Server"  # Your broker's server

    initialize_mt5(account, password, server)
    
    symbol = "EURUSD"
    output_path = f'../data/{symbol}_2_hours_data.csv'
    run_streaming_data(symbol, output_path)

    shutdown_mt5()