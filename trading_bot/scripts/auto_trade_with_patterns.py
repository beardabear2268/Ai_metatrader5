import MetaTrader5 as mt5
import pandas as pd
import logging
import time
import joblib
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

def load_model(file_path):
    model = joblib.load(file_path)
    logging.info("Model loaded from {}".format(file_path))
    return model

def preprocess_data(df):
    df = df.dropna()
    df['mid'] = (df['ask'] + df['bid']) / 2
    df = df[['time', 'mid']]
    return df

def make_decision(model, df):
    df = preprocess_data(df)
    X = df[['mid']]
    prediction = model.predict(X)
    return "buy" if prediction[-1] == 1 else "sell"

def execute_trade(symbol, action):
    price = mt5.symbol_info_tick(symbol).ask if action == "buy" else mt5.symbol_info_tick(symbol).bid
    order_type = mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL
    deviation = 20

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.1,
        "type": order_type,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.error(f"Order failed, retcode = {result.retcode}")
    else:
        logging.info(f"Order executed: {result}")

if __name__ == "__main__":
    logging.basicConfig(filename='../logs/auto_trade.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    
    account = 7052173 
    password = "Hilary2268!"
    server = "FPMarketsLLC-Demo Server"  # Your broker's server

    initialize_mt5(account, password, server)
    
    symbol = "EURUSD"
    model_path = '../models/trained_realtime_model.pkl'
    model = load_model(model_path)
    
    for _ in range(120):  # Run for 2 hours, checking every minute
        df = fetch_realtime_data(symbol)
        if df is not None and not df.empty:
            df = recognize_patterns(df)
            df = implement_strategy(df, strategy='ma')  # Example: Moving Average strategy
            action = make_decision(model, df)
            execute_trade(symbol, action)
            append_to_csv(df, f'../data/{symbol}_continuous_data.csv')

        time.sleep(60)  # Wait for 1 minute
        
    shutdown_mt5()