import logging
import time
from datetime import datetime, time as dt_time, timedelta
import schedule
from data_parsing import fetch_ohlcv_data, add_technical_indicators, filter_data, generate_features_labels
from detection import detect_patterns, enhanced_stop_loss, calculate_risk_reward, complex_probability
from model_training import load_model, save_model, simulate_trade, execute_trade, train_model, validate_model
from mq4_integration import load_advisor, load_trainer, load_data_parser
from data_fetching import fetch_ohlcv_data_concurrently
from advisor import get_ai_suggestions, decide_on_trade
from symbol_fetching import fetch_symbols

# Set up logging
logging.basicConfig(filename='trading_bot.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

TRADING_SESSION_DURATION = 7200  # 2 hours in seconds
BREAK_DURATION = 900  # 15 minutes in seconds

def initialize_strategies():
    try:
        strategies = scrape_trading_strategies()
        logging.info("Fetched strategies: %s", strategies)
        return strategies
    except Exception as e:
        logging.error(f"Failed to fetch strategies: {e}")
        return []

def load_mq4_files():
    try:
        logging.info("Loading MQ4 files (trainer, advisor, data parser)...")
        load_advisor("advisor.mq4")
        load_trainer("trainer.mq4")
        load_data_parser("data_parser.mq4")
    except Exception as e:
        logging.error(f"Failed to load MQ4 files: {e}")

def perform_trading_operations(symbols):
    try:
        strategies = initialize_strategies()
        model = load_model()
        df = fetch_ohlcv_data_concurrently(symbols, '1m')

        if df.empty:
            logging.warning("Fetched DataFrame is empty. Aborting trading operations.")
            return

        df = add_technical_indicators(df)
        df = detect_patterns(df)
        df['pattern_detected'] = True  # Assuming every row detects pattern, replace with actual detection logic
        df = enhanced_stop_loss(df)
        df = calculate_risk_reward(df)
        df = complex_probability(df)
        
        df = filter_data(df)
        X, y = generate_features_labels(df)

        # Integrating AI suggestions for final decision making
        suggestions = get_ai_suggestions(X)
        X = apply_ai_suggestions(X, suggestions)

        # Training the model
        new_model, new_accuracy = train_model(X, y)
        new_avg_score = validate_model(new_model, X, y)

        # Save if new model is better
        existing_model = load_model()
        if existing_model is not None:
            existing_avg_score = validate_model(existing_model, X, y)
            if new_avg_score > existing_avg_score:
                logging.info("New model's performance is better. Replacing the existing model.")
                save_model(new_model, 'btc_trading_model.pkl')
            else:
                logging.info("Existing model's performance is better. Retaining the existing model.")
        else:
            save_model(new_model, 'btc_trading_model.pkl')

        trade_start_time = datetime.now()
        for _, row in df.iterrows():
            if decide_on_trade(row, df):
                result = simulate_trade(row.to_dict(), new_model)
                execute_trade(result, trade_start_time)
        logging.info("Completed trading operations.")
    except Exception as e:
        logging.error(f"Error during trading operations: {e}")

def job():
    try:
        current_time = datetime.now().time()
        start_time = dt_time(9, 0)  # 9:00 AM
        end_time = dt_time(18, 0)  # 6:00 PM

        if start_time <= current_time <= end_time:
            symbols = fetch_symbols()
            if symbols:
                perform_trading_operations(symbols[:50])  # Limiting to 50 symbols for performance
            else:
                logging.warning("No symbols fetched; skipping this trading session.")
    except Exception as e:
        logging.error(f"Error in scheduled job: {e}")

def main():
    try:
        load_mq4_files()
        schedule.every().monday.at("09:00").do(job)
        schedule.every().tuesday.at("09:00").do(job)
        schedule.every().wednesday.at("09:00").do(job)
        schedule.every().thursday.at("09:00").do(job)
        schedule.every().friday.at("09:00").do(job)

        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
