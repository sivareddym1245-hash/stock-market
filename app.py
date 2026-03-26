from fastapi import FastAPI
from data import get_stock_data, preprocess_data
app = FastAPI()
COMPANIES = ["INFY.NS", "TCS.NS", "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
@app.get("/companies")
def get_companies():
    return COMPANIES



@app.get("/summary/{symbol}")
def get_summary(symbol: str):
    df = get_stock_data(symbol)
    return{
        "52 High": float(df['Close'].max()),
        "52 Low": float(df['Close'].min()),
        "Average Close": float(df['Close'].mean())
    }

@app.get("/compare")
def compare(symbol1: str, symbol2: str):
    df1 = get_stock_data(symbol1)
    df2 = get_stock_data(symbol2)

    return{
        symbol1: float(df1['Close'].iloc[-1]),
        symbol2: float(df2['Close'].iloc[-1])
    }
@app.get("/data/{symbol}")
def get_data(symbol: str):
    df = get_stock_data(symbol)

    if df.empty:
        return {"error": "Invalid symbol"}

    try:
        df = preprocess_data(df)
    except Exception as e:
        return {"error": str(e)}

    # Safe column handling
    if 'Date' in df.columns:
        df['Date'] = df['Date'].astype(str)

    return df.tail(30).to_dict(orient="records")

@app.get("/summary/{symbol}")
def get_summary(symbol: str):
    df = get_stock_data(symbol)

    if df.empty:
        return {"error": "Invalid symbol"}

    return {
        "52 High": float(df['Close'].max()),
        "52 Low": float(df['Close'].min()),
        "Average Close": float(df['Close'].mean())
    }
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)