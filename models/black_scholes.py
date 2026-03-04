import numpy as np
from scipy.stats import norm


def d1_d2(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def price(S, K, T, r, sigma, option="call"):
    d1, d2 = d1_d2(S, K, T, r, sigma)
    if option == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def greeks(S, K, T, r, sigma, option="call"):
    d1, d2 = d1_d2(S, K, T, r, sigma)
    sqrt_T = np.sqrt(T)
    pdf_d1 = norm.pdf(d1)

    delta = norm.cdf(d1) if option == "call" else norm.cdf(d1) - 1
    gamma = pdf_d1 / (S * sigma * sqrt_T)
    vega  = S * pdf_d1 * sqrt_T / 100          # per 1% move in vol
    theta_call = (-(S * pdf_d1 * sigma) / (2 * sqrt_T)
                  - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    theta = theta_call if option == "call" else (
        theta_call + r * K * np.exp(-r * T) / 365)
    rho_call = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    rho = rho_call if option == "call" else (
        -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100)

    return {"Delta": delta, "Gamma": gamma, "Vega": vega,
            "Theta": theta, "Rho": rho}