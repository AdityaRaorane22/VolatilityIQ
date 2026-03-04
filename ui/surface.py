import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from models.implied_vol import implied_vol
from data.fetch import get_chain, get_expiries, time_to_expiry


def render_surface(df: pd.DataFrame, S: float, T: float, r: float, option: str):
    st.subheader("Implied Volatility Surface")

    ticker   = st.session_state.get("ticker", "AAPL")
    expiries = get_expiries(ticker)[:8]          # cap at 8 expiries for speed

    records = []
    for exp in expiries:
        t   = time_to_expiry(exp)
        try:
            chain = get_chain(ticker, exp, option)
        except Exception:
            continue
        for _, row in chain.iterrows():
            mid = (row["bid"] + row["ask"]) / 2 if row["bid"] > 0 else row["lastPrice"]
            if mid <= 0:
                continue
            iv = implied_vol(mid, S, row["strike"], t, r, option)
            if not np.isnan(iv) and 0.01 < iv < 5:
                records.append({"Strike": row["strike"], "T": round(t, 4), "IV": iv * 100})

    if not records:
        st.warning("Not enough data to render surface.")
        return

    surface = pd.DataFrame(records)
    pivot   = surface.pivot_table(index="Strike", columns="T", values="IV", aggfunc="mean")

    fig = go.Figure(data=[go.Surface(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale="Viridis",
        colorbar=dict(title="IV (%)"),
    )])
    fig.update_layout(
        scene=dict(
            xaxis_title="Time to Expiry (yrs)",
            yaxis_title="Strike",
            zaxis_title="Implied Vol (%)",
        ),
        height=550,
        template="plotly_dark",
    )
    st.plotly_chart(fig, use_container_width=True)