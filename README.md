# 📈 Stock Portfolio Tracker

A command-line Python application that lets you track your stock holdings and calculate portfolio value.

## Features

- Interactive CLI — enter tickers and share quantities one by one
- Hardcoded real-time-style prices for 8 popular stocks (AAPL, TSLA, GOOG, MSFT, AMZN, NVDA, META, NFLX)
- Calculates per-stock and grand-total portfolio values
- Exports a formatted CSV summary (`portfolio.csv`)
- Input validation with helpful error messages and recursive re-prompting

## Supported Tickers

| Ticker | Company                  | Price (USD) |
|--------|--------------------------|-------------|
| AAPL   | Apple Inc.               | $180.00     |
| TSLA   | Tesla Inc.               | $250.00     |
| GOOG   | Alphabet Inc. (Google)   | $175.00     |
| MSFT   | Microsoft Corporation    | $420.00     |
| AMZN   | Amazon.com Inc.          | $185.00     |
| NVDA   | NVIDIA Corporation       | $875.00     |
| META   | Meta Platforms Inc.      | $480.00     |
| NFLX   | Netflix Inc.             | $630.00     |

## Getting Started

### Prerequisites

- Python 3.10+ (uses `str | None` union type hints)

### Run

```bash
python portfolio_tracker.py
```

### Example Session

```
==========================================================
   💼  STOCK PORTFOLIO TRACKER
==========================================================

  📈  Available Stocks:
  Ticker      Price (USD)
  ----------------------
  AAPL           $180.00
  ...

  Enter stock ticker (or 'done' / 'exit' to finish): AAPL
  Enter quantity (shares) of AAPL: 10
  ✅  Added  10 share(s) of AAPL.

  Enter stock ticker (or 'done' / 'exit' to finish): done

==========================================================
   📊  PORTFOLIO SUMMARY
==========================================================
  Ticker      Shares        Price    Total Value
  ------------------------------------------------
  AAPL            10      $180.00      $1,800.00
  ------------------------------------------------
  GRAND TOTAL                          $1,800.00
==========================================================

  💾  Portfolio saved to 'portfolio.csv'  [2026-06-30 19:00:00]
  Thank you for using the Stock Portfolio Tracker! 🚀
```

## Project Structure

```
stocks_portfolio/
├── portfolio_tracker.py   # Main application
├── .gitignore
└── README.md
```

## Concepts Demonstrated

- **Dictionaries** — ticker → price lookup, portfolio accumulation
- **Lists of dicts** — row-based data structure for display and CSV output
- **File I/O** — writing CSV with Python's `csv.DictWriter`
- **Exception handling** — `try/except ValueError` for quantity input
- **Type hints** — `dict[str, int]`, `list[dict]`, `str | None`
- **Recursive functions** — re-prompting on invalid ticker input

## License

MIT
