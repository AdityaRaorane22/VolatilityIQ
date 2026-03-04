# VolatilityIQ

Real-time options pricing and volatility analytics dashboard built with Black-Scholes, Newton-Raphson IV solving, and live market data.

---

## Features

- **Black-Scholes Pricing** — call/put pricing using the closed-form BS formula
- **Implied Volatility Solver** — Newton-Raphson iteration to back out market IV from option prices
- **Option Greeks** — Delta, Gamma, Theta, Vega, Rho with live sensitivity curves
- **Volatility Surface** — 3D surface across strikes and expiries using live options chain data
- **Options Chain Table** — BS price vs market mid with edge highlighting

---

## Math Overview

### Black-Scholes Formula

```
d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
d2 = d1 - σ√T

Call = S·N(d1) - K·e^(-rT)·N(d2)
Put  = K·e^(-rT)·N(-d2) - S·N(-d1)
```

### Greeks

| Greek | Formula |
|-------|---------|
| Delta | N(d1) for call, N(d1)-1 for put |
| Gamma | N'(d1) / (S·σ·√T) |
| Vega  | S·N'(d1)·√T |
| Theta | -(S·N'(d1)·σ)/(2√T) - rKe^(-rT)N(d2) |
| Rho   | KTe^(-rT)·N(d2) |

### Implied Volatility (Newton-Raphson)

```
σ(n+1) = σ(n) - [BS(σ(n)) - market_price] / Vega(σ(n))
```
Converges in ~5 iterations typically.

---

## Setup

```bash
git clone https://github.com/AdityaRaorane22/VolatilityIQ
cd VolatilityIQ
pip install -r requirements.txt
streamlit run app.py
```

---

## Folder Structure

```
VolatilityIQ/
├── app.py                  # Streamlit entry point
├── requirements.txt
├── models/
│   ├── black_scholes.py    # BS formula + Greeks
│   └── implied_vol.py      # IV solver (Newton-Raphson)
├── data/
│   └── fetch.py            # yfinance live data
└── ui/
    ├── chain.py            # Options chain table
    ├── greeks.py           # Greeks dashboard
    └── surface.py          # 3D vol surface
```

---

## Usage

1. Enter a ticker (e.g. `AAPL`, `TSLA`, `SPY`)
2. Select expiry date and option type
3. Explore the three tabs — Chain, Greeks, Surface
