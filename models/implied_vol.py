import numpy as np
from models.black_scholes import price, greeks


def implied_vol(market_price, S, K, T, r, option="call", tol=1e-6, max_iter=100):
    """Newton-Raphson solver for implied volatility."""
    sigma = 0.2  # initial guess

    for _ in range(max_iter):
        p    = price(S, K, T, r, sigma, option)
        vega = greeks(S, K, T, r, sigma, option)["Vega"] * 100  # undo /100 scaling

        diff = p - market_price
        if abs(diff) < tol:
            return sigma
        if vega < 1e-8:
            break
        sigma -= diff / vega

    return np.nan  # did not converge