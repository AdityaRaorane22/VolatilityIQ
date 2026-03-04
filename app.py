import streamlit as st
from data.fetch import get_spot, get_expiries, get_chain, time_to_expiry
from models.black_scholes import price, greeks
from ui.chain import render_chain
from ui.greeks import render_greeks
from ui.surface import render_surface

st.set_page_config(page_title="VolatilityIQ", layout="wide")
st.title("VolatilityIQ — Options Pricing & Volatility Analytics")

# ── Sidebar inputs ──────────────────────────────────────────
with st.sidebar:
    st.header("Parameters")
    ticker  = st.text_input("Ticker", value="AAPL").upper()
    r       = st.slider("Risk-free Rate (%)", 0.0, 10.0, 5.0) / 100
    option  = st.radio("Option Type", ["call", "put"])

    expiries = get_expiries(ticker)
    expiry   = st.selectbox("Expiry", expiries)

# ── Fetch live data ─────────────────────────────────────────
S  = get_spot(ticker)
T  = time_to_expiry(expiry)
df = get_chain(ticker, expiry, option)

st.metric("Spot Price", f"${S:.2f}")

# ── Tabs ─────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Options Chain", "Greeks", "Vol Surface"])

with tab1:
    render_chain(df, S, T, r, option)

with tab2:
    render_greeks(S, T, r, option)

with tab3:
    render_surface(df, S, T, r, option)