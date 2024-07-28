import pandas as pd

def calculate_moving_average(df, window):
    df[f'ma_{window}'] = df['close'].rolling(window=window).mean()
    return df

def calculate_bollinger_bands(df, window=20):
    df['bb_mean'] = df['close'].rolling(window=window).mean()
    df['bb_std'] = df['close'].rolling(window=window).std()
    df['upper_bb'] = df['bb_mean'] + (2 * df['bb_std'])
    df['lower_bb'] = df['bb_mean'] - (2 * df['bb_std'])
    return df

def calculate_rsi(df, window=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    return df

def recognize_patterns(df):
    df = calculate_moving_average(df, 20)
    df = calculate_bollinger_bands(df, 20)
    df = calculate_rsi(df, 14)
    return df