import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Stock Explorer", layout="wide", page_icon="📈")
st.title("📈 Stock Price Explorer")
st.caption("Compare how the big tech stocks have grown since Jan 2018 — live data, updated daily.")

TICKERS = ["AAPL", "MSFT", "GOOG", "AMZN", "META", "NFLX"]


@st.cache_data(ttl="1d")
def load_data():
    raw = yf.download(TICKERS, start="2018-01-01", progress=False)["Close"]
    raw = raw.dropna(how="all").reset_index()
    raw = raw.rename(columns={"Date": "date"})
    return raw


df = load_data()
tickers = [c for c in df.columns if c != "date"]

st.sidebar.header("Controls")
chosen = st.sidebar.multiselect("Choose stocks", tickers, default=["AAPL", "MSFT", "GOOG"])

min_date, max_date = df["date"].min().to_pydatetime(), df["date"].max().to_pydatetime()
date_range = st.sidebar.slider(
    "Date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="MMM YYYY",
)

st.sidebar.divider()
invest_amount = st.sidebar.number_input("What if I invested $", min_value=100, value=1000, step=100)

if not chosen:
    st.warning("Pick at least one stock from the sidebar.")
    st.stop()

mask = (df["date"] >= date_range[0]) & (df["date"] <= date_range[1])
view = df.loc[mask].reset_index(drop=True)

# Re-normalize to 1.0 at the start of the selected date range so growth % reflects the window picked
norm = view.copy()
for t in tickers:
    norm[t] = view[t] / view[t].iloc[0]

st.info(
    "💡 Did you know? Apple's iPhone, launched in 2007, remains the company's single "
    "largest revenue driver — generating more annual revenue on its own than most "
    "Fortune 500 companies make in total."
)

st.info(
    "🎬 Did you know? In August 2008, a database corruption knocked Netflix's DVD "
    "shipping offline for three days — the incident pushed Netflix to move its "
    "infrastructure to Amazon Web Services, a bet that helped turn AWS into the "
    "cloud-computing giant it is today."
)

# Key metrics: growth for each chosen stock over the selected window
cols = st.columns(len(chosen))
growth_by_ticker = {t: (norm[t].iloc[-1] - 1) * 100 for t in chosen}
for col, t in zip(cols, chosen):
    col.metric(t, f"{norm[t].iloc[-1]:.2f}x", f"{growth_by_ticker[t]:+.1f}%")

best = max(growth_by_ticker, key=growth_by_ticker.get)
worst = min(growth_by_ticker, key=growth_by_ticker.get)
st.success(f"🏆 Best performer in this window: **{best}** ({growth_by_ticker[best]:+.1f}%)")

# Line chart comparing normalized growth
fig = px.line(norm, x="date", y=chosen, title="Normalized price over time (1.0 = start of range)")
fig.update_layout(legend_title_text="Stock", yaxis_title="Growth multiple", xaxis_title="Date")
st.plotly_chart(fig, use_container_width=True)

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Total growth by stock")
    bar_df = pd.DataFrame({"Stock": list(growth_by_ticker.keys()), "Growth %": list(growth_by_ticker.values())})
    bar_fig = px.bar(bar_df, x="Stock", y="Growth %", color="Stock", text_auto=".1f")
    st.plotly_chart(bar_fig, use_container_width=True)

with c2:
    st.subheader("🌪️ Volatility (most up-and-down)")
    vol = {t: norm[t].pct_change().std() * 100 for t in chosen}
    vol_df = pd.DataFrame({"Stock": list(vol.keys()), "Volatility %": list(vol.values())}).sort_values(
        "Volatility %", ascending=False
    )
    vol_fig = px.bar(vol_df, x="Stock", y="Volatility %", color="Stock", text_auto=".2f")
    st.plotly_chart(vol_fig, use_container_width=True)
    most_volatile = vol_df.iloc[0]["Stock"]
    st.caption(f"Most volatile in this window: **{most_volatile}**")

st.divider()
st.subheader("💸 What if I had invested?")
invest_cols = st.columns(len(chosen))
for col, t in zip(invest_cols, chosen):
    final_value = invest_amount * norm[t].iloc[-1]
    col.metric(
        f"${invest_amount:,.0f} in {t}",
        f"${final_value:,.0f}",
        f"{growth_by_ticker[t]:+.1f}%",
    )
