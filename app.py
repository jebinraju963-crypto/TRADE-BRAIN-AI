import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="TRADE BRAIN AI",
    page_icon="📈",
    layout="wide"
)

# Demo stock data only
stocks = {
    "RELIANCE": {"price": 1450.0, "change": 1.8},
    "TCS": {"price": 3200.0, "change": 0.7},
    "INFY": {"price": 1550.0, "change": -0.8},
    "HDFCBANK": {"price": 1750.0, "change": 1.2},
    "ICICIBANK": {"price": 1250.0, "change": 2.1},
    "SBIN": {"price": 780.0, "change": -1.2},
    "ITC": {"price": 420.0, "change": 0.5},
    "BHARTIARTL": {"price": 1850.0, "change": 1.5}
}

if "cash" not in st.session_state:
    st.session_state.cash = 100000.0

if "holdings" not in st.session_state:
    st.session_state.holdings = {}

if "trades" not in st.session_state:
    st.session_state.trades = []

st.title("📈 TRADE BRAIN AI")
st.caption("Smart Market. Smarter Decisions.")

st.warning(
    "DEMO MODE: All prices and signals are simulated. "
    "This is not live NSE market data."
)

st.subheader("💰 Paper Trading Account")

col1, col2, col3 = st.columns(3)

invested = sum(
    item["qty"] * stocks[symbol]["price"]
    for symbol, item in st.session_state.holdings.items()
)

col1.metric("Virtual Balance", f"₹{st.session_state.cash:,.2f}")
col2.metric("Holdings Value", f"₹{invested:,.2f}")
col3.metric(
    "Portfolio Value",
    f"₹{st.session_state.cash + invested:,.2f}"
)

st.divider()

st.subheader("📊 NSE Watchlist (Simulated)")

watchlist = []

for symbol, data in stocks.items():
    change = data["change"]

    if change >= 1.5:
        signal = "BUY (Demo)"
    elif change <= -1:
        signal = "SELL (Demo)"
    else:
        signal = "WAIT"

    watchlist.append({
        "Stock": symbol,
        "Demo Price": data["price"],
        "Change %": change,
        "Demo Signal": signal
    })

st.dataframe(
    pd.DataFrame(watchlist),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("🤖 Paper Trading")

symbol = st.selectbox("Select NSE Stock", list(stocks.keys()))
quantity = st.number_input(
    "Quantity",
    min_value=1,
    max_value=1000,
    value=1
)

price = stocks[symbol]["price"]
st.write(f"Demo Price: ₹{price:,.2f}")
st.write(f"Order Value: ₹{price * quantity:,.2f}")

buy_col, sell_col = st.columns(2)

with buy_col:
    if st.button("🟢 PAPER BUY", use_container_width=True):
        cost = price * quantity

        if cost <= st.session_state.cash:
            old = st.session_state.holdings.get(
                symbol, {"qty": 0, "avg": 0.0}
            )

            new_qty = old["qty"] + quantity
            new_avg = (
                old["qty"] * old["avg"] + cost
            ) / new_qty

            st.session_state.holdings[symbol] = {
                "qty": new_qty,
                "avg": new_avg
            }

            st.session_state.cash -= cost

            st.session_state.trades.append({
                "Time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "Stock": symbol,
                "Side": "BUY",
                "Quantity": quantity,
                "Price": price
            })

            st.success("Paper BUY order completed!")
        else:
            st.error("Insufficient virtual balance.")

with sell_col:
    if st.button("🔴 PAPER SELL", use_container_width=True):
        holding = st.session_state.holdings.get(
            symbol, {"qty": 0, "avg": 0.0}
        )

        if holding["qty"] >= quantity:
            st.session_state.cash += price * quantity
            holding["qty"] -= quantity

            if holding["qty"] == 0:
                del st.session_state.holdings[symbol]
            else:
                st.session_state.holdings[symbol] = holding

            st.session_state.trades.append({
                "Time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "Stock": symbol,
                "Side": "SELL",
                "Quantity": quantity,
                "Price": price
            })

            st.success("Paper SELL order completed!")
        else:
            st.error("Not enough shares in your paper holdings.")

st.divider()

st.subheader("📁 My Portfolio")

portfolio = []

for symbol, item in st.session_state.holdings.items():
    portfolio.append({
        "Stock": symbol,
        "Quantity": item["qty"],
        "Average Price": item["avg"],
        "Demo Current Price": stocks[symbol]["price"]
    })

if portfolio:
    st.dataframe(pd.DataFrame(portfolio), use_container_width=True)
else:
    st.info("No paper holdings yet.")

st.subheader("📜 Paper Trade History")

if st.session_state.trades:
    st.dataframe(
        pd.DataFrame(st.session_state.trades),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No paper trades yet.")

st.divider()

st.subheader("⚙️ Risk Management Settings")

stop_loss = st.slider("Illustrative Stop Loss (%)", 0.5, 5.0, 1.0)
daily_limit = st.slider("Illustrative Daily Loss Limit (%)", 0.5, 5.0, 1.0)

st.write(f"Selected Stop Loss: {stop_loss}%")
st.write(f"Selected Daily Loss Limit: {daily_limit}%")

st.caption(
    "These settings are illustrative only; they do not currently "
    "automatically enforce stop-loss or daily-loss restrictions."
)

st.divider()

st.caption(
    "TRADE BRAIN AI | Phase 1 | Paper Trading Only | "
    "No broker connection | No live orders"
)
