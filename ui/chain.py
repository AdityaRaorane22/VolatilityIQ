import streamlit as st
import pandas as pd
from models.black_scholes import price, greeks as bs_greeks


def render_chain(df: pd.DataFrame, S: float, T: float, r: float, option: str):
    st.subheader("Options Chain — BS Price vs Market Price")

    rows = []
    for _, row in df.iterrows():
        K      = row["strike"]
        sigma  = row["market_iv"]
        mid    = (row["bid"] + row["ask"]) / 2 if row["bid"] > 0 else row["lastPrice"]

        bs     = price(S, K, T, r, sigma, option)
        g      = bs_greeks(S, K, T, r, sigma, option)
        edge   = round(bs - mid, 4)

        rows.append({
            "Strike":     K,
            "Mid":        round(mid, 2),
            "BS Price":   round(bs, 2),
            "Edge":       edge,
            "IV (%)":     round(sigma * 100, 2),
            "Delta":      round(g["Delta"], 4),
            "Gamma":      round(g["Gamma"], 4),
            "Theta":      round(g["Theta"], 4),
            "Vega":       round(g["Vega"], 4),
        })

    result = pd.DataFrame(rows)

    # colour edge: green = BS > market, red = BS < market
    def colour_edge(val):
        color = "green" if val > 0 else "red"
        return f"color: {color}"

    st.dataframe(
        result.style.applymap(colour_edge, subset=["Edge"]),
        use_container_width=True,
        height=500,
    )