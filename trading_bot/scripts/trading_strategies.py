import pandas as pd

def moving_average_strategy(df):
    df['signal'] = 0
    df['signal'][df['ma_20'] > df['close']] = 1
    df['signal'][df['ma_20'] < df['close']] = -1
    return df

def bollinger_band_strategy(df):
    df['signal'] = 0
    df['signal'][df['close'] > df['upper_bb']] = -1
    df['signal'][df['close'] < df['lower_bb']] = 1
    return df

def rsi_strategy(df):
    df['signal'] = 0
    df['signal'][df['rsi'] > 70] = -1
    df['signal'][df['rsi'] < 30] = 1
    return df

def implement_strategy(df, strategy='ma'):
    if strategy == 'ma':
        df = moving_average_strategy(df)
    elif strategy == 'bb':
        df = bollinger_band_strategy(df)
    elif strategy == 'rsi':
        df = rsi_strategy(df)
    return df