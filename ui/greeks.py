import streamlit as st
import numpy as np
import plotly.graph_objects as go
from models.black_scholes import greeks as bs_greeks


def render_greeks(S: float, T: float, r: float, option: str):
    st.subheader("Greeks — Sensitivity Analysis")

    col1, col2 = st.columns(2)
    with col1:
        K     = st.number_input("Strike (K)", value=round(S), step=1)
        sigma = st.slider("Volatility σ (%)", 5, 100, 25) / 100

    greek_names = ["Delta", "Gamma", "Vega", "Theta", "Rho"]
    spot_range  = np.linspace(S * 0.7, S * 1.3, 200)

    fig = go.Figure()
    for greek in greek_names:
        values = [bs_greeks(s, K, T, r, sigma, option)[greek] for s in spot_range]
        fig.add_trace(go.Scatter(x=spot_range, y=values, name=greek, mode="lines"))

    fig.update_layout(
        xaxis_title="Spot Price",
        yaxis_title="Greek Value",
        legend_title="Greek",
        height=450,
        template="plotly_dark",
    )
    st.plotly_chart(fig, use_container_width=True)

    # snapshot at current spot
    st.markdown("**Greeks at current spot:**")
    g = bs_greeks(S, K, T, r, sigma, option)
    cols = st.columns(5)
    for col, (name, val) in zip(cols, g.items()):
        col.metric(name, round(val, 4))