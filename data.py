

import yfinance as yf

import pandas as pd


def get_stock_data(symbol):
    df = yf.download(symbol, period="1y")
    if df.empty:
        return {"error": "Invalid stock symbol"}
    df.reset_index(inplace=True)
    return df

def preprocess_data(df):
    # Fix tuple column names
    if isinstance(df.columns, tuple) or isinstance(df.columns[0], tuple):
        df.columns = [col[0] for col in df.columns]

    # OR safer universal fix:
    df.columns = [str(col).split(",")[0].replace("(", "").replace("'", "") for col in df.columns]

    # Daily Return
    df['Daily Return'] = (df['Close'] - df['Open']) / df['Open']

    # 7-day Moving Average
    df['7 Day MA'] = df['Close'].rolling(7).mean()

    # Fill NaN
    

    df['30 day MA'] = df['Close'].rolling(30).mean()
    df['52 High'] = df['Close'].rolling(252).max()
    df['52 Low'] = df['Close'].rolling(252).min()
    df.fillna(0, inplace=True)
    return df