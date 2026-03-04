import yfinance as yf
import pandas as pd
from datetime import date


def get_spot(ticker: str) -> float:
    return yf.Ticker(ticker).fast_info["last_price"]


def get_chain(ticker: str, expiry: str, option: str = "call") -> pd.DataFrame:
    """Return options chain for a given expiry. option = 'call' | 'put'."""
    tk  = yf.Ticker(ticker)
    opt = tk.option_chain(expiry)
    df  = opt.calls if option == "call" else opt.puts
    df  = df[["strike", "lastPrice", "bid", "ask", "impliedVolatility", "volume"]].copy()
    df.rename(columns={"impliedVolatility": "market_iv"}, inplace=True)
    return df.reset_index(drop=True)


def get_expiries(ticker: str) -> tuple:
    return yf.Ticker(ticker).options


def time_to_expiry(expiry: str) -> float:
    """Returns T in years from today."""
    exp  = date.fromisoformat(expiry)
    diff = (exp - date.today()).days
    return max(diff / 365, 1e-6)