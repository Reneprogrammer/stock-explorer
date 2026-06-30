# 📈 Stock Price Explorer

A simple Streamlit app for comparing how the big tech stocks (AAPL, MSFT, GOOG, AMZN, META, NFLX) have grown since January 2018, using live data updated daily.

**Live app:** _add your Streamlit Cloud URL here_

## Features

- Pick any combination of stocks to compare
- Date-range slider to zoom into a specific period
- Growth metrics (x-multiple and %) per stock, normalized to the start of the selected range
- 🏆 Automatic "best performer" callout
- 📊 Bar chart of total growth by stock
- 🌪️ Volatility indicator — which stock bounced around the most
- 💸 "What if I invested $X?" calculator
- 💡 Real-world "Did you know?" facts about Apple and Netflix

## Architecture

```mermaid
flowchart LR
    A[Live stock data<br/>via yfinance] --> B[Streamlit app<br/>app.py]
    B --> C[GitHub repo]
    C --> D[Streamlit<br/>Community Cloud]
    D --> E[User's browser]
```

The app fetches live daily stock prices at runtime with `yfinance` (cached for a day via `@st.cache_data`), so the data is always current through today — no static file to maintain. The code lives in a public GitHub repo, which Streamlit Community Cloud watches and deploys automatically on every push.

### User journey

```mermaid
journey
    title Analyst exploring stock growth
    section Open the app
      Visit the live URL: 5: User
      App loads with default stocks (AAPL, MSFT, GOOG): 5: User
    section Explore
      Pick stocks to compare: 4: User
      Drag the date-range slider: 4: User
      Read the "Did you know?" facts: 5: User
    section Decide
      Spot the best performer callout: 5: User
      Check the volatility chart: 4: User
      Try the "what if I invested $X" calculator: 5: User
    section Share
      Send the link to the boss: 5: User
```

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech stack

- [Streamlit](https://streamlit.io/) — web UI
- [Plotly](https://plotly.com/python/) — charts
- [yfinance](https://github.com/ranaroussi/yfinance) — live stock price data
- [pandas](https://pandas.pydata.org/) — data wrangling
