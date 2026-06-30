import csv
from datetime import datetime


#  HARDCODED STOCK PRICES (dictionary lookup)
#  Key   → stock ticker symbol (str, uppercase)
#  Value → price per share in USD (float)

STOCK_PRICES: dict[str, float] = {
    "AAPL":  180.00,   # Apple Inc.
    "TSLA":  250.00,   # Tesla Inc.
    "GOOG":  175.00,   # Alphabet Inc. (Google)
    "MSFT":  420.00,   # Microsoft Corporation
    "AMZN":  185.00,   # Amazon.com Inc.
    "NVDA":  875.00,   # NVIDIA Corporation
    "META":  480.00,   # Meta Platforms Inc.
    "NFLX":  630.00,   # Netflix Inc.
}

# Output file name for the CSV portfolio summary
OUTPUT_CSV: str = "portfolio.csv"


def display_available_tickers() -> None:
    """Print all available stock tickers and their prices."""
    print("\n  📈  Available Stocks:")
    print(f"  {'Ticker':<8}  {'Price (USD)':>12}")
    print("  " + "-" * 22)
    for ticker, price in STOCK_PRICES.items():
        print(f"  {ticker:<8}  ${price:>11,.2f}")
    print()


def get_ticker_input() -> str | None:
    """
    Returns:
        The uppercased ticker string, or None if the user
        wants to exit the input loop.
    """
    raw = input("  Enter stock ticker (or 'done' / 'exit' to finish): ").strip()

    # Normalise to uppercase
    ticker = raw.upper()

    # Sentinel values that signal the user is done adding stocks
    if ticker in ("DONE", "EXIT", "Q", "QUIT", ""):
        return None

    # Dictionary lookup
    if ticker not in STOCK_PRICES:
        print(f"\n  ⚠️  '{raw}' was not found in our price list.")
        display_available_tickers()
        return get_ticker_input()   # Recursively re-prompt for a valid ticker

    return ticker


def get_quantity_input(ticker: str) -> int | None:
    """
    Prompt the user for the number of shares they own.

    Uses a try-except block to handle ValueError when the user
    types letters instead of a whole number.

    Args:
        ticker: The validated stock ticker (used only for display).

    Returns:
        A positive integer quantity, or None to cancel this entry.
    """
    while True:
        raw = input(f"  Enter quantity (shares) of {ticker}: ").strip()

        if raw.lower() in ("exit", "done", "q", "quit", ""):
            return None

        try:
            quantity = int(raw)           # raises ValueError for non-integers
            if quantity <= 0:
                print("  ⚠️  Please enter a positive whole number of shares.")
                continue
            return quantity

        except ValueError:
            # Gracefully inform the user without crashing
            print(f"  ⚠️  '{raw}' is not a valid number. "
                  "Please enter a whole number (e.g. 10).")


def build_portfolio() -> dict[str, int]:
    """
    Run the interactive input loop and collect the user's holdings.

    Returns:
        A dictionary mapping ticker → total shares owned.
        If a ticker is entered more than once the quantities are summed.
    """
    portfolio: dict[str, int] = {}

    print("\n" + "=" * 58)
    print("   💼  STOCK PORTFOLIO TRACKER")
    print("=" * 58)
    display_available_tickers()
    print("  Type 'done' or 'exit' at any prompt to finish.\n")

    while True:
        ticker = get_ticker_input()
        if ticker is None:
            break   # User chose to stop adding stocks

        quantity = get_quantity_input(ticker)
        if quantity is None:
            break   # User chose to stop mid-entry

        # Accumulate shares if the same ticker is entered more than once
        portfolio[ticker] = portfolio.get(ticker, 0) + quantity
        print(f"  ✅  Added  {quantity:,} share(s) of {ticker}.\n")

    return portfolio


#  CALCULATION
def calculate_portfolio_value(
    portfolio: dict[str, int]
) -> list[dict]:
    """
    Compute per-stock and total portfolio values.

    Arithmetic:  Total Value = Quantity × Price per Share

    Args:
        portfolio: Mapping of ticker → shares owned.

    Returns:
        A list of row-dictionaries ready for display / file output.
    """
    rows: list[dict] = []
    for ticker, quantity in portfolio.items():
        price       = STOCK_PRICES[ticker]          # dictionary lookup
        total_value = quantity * price              # core arithmetic
        rows.append({
            "ticker":      ticker,
            "quantity":    quantity,
            "price":       price,
            "total_value": total_value,
        })
    return rows



#  DISPLAY
def print_summary(rows: list[dict]) -> float:
    """
    Print a formatted summary table to the console.

    Args:
        rows: List of per-stock dictionaries from calculate_portfolio_value().

    Returns:
        The grand total portfolio value (float).
    """
    grand_total: float = 0.0

    # Table header
    print("\n" + "=" * 58)
    print("   📊  PORTFOLIO SUMMARY")
    print("=" * 58)
    print(f"  {'Ticker':<8}  {'Shares':>8}  {'Price':>12}  {'Total Value':>14}")
    print("  " + "-" * 48)

    for row in rows:
        grand_total += row["total_value"]
        print(
            f"  {row['ticker']:<8}"
            f"  {row['quantity']:>8,}"
            f"  ${row['price']:>11,.2f}"
            f"  ${row['total_value']:>13,.2f}"
        )

    # Grand total row
    print("  " + "-" * 48)
    print(f"  {'GRAND TOTAL':<30}  ${grand_total:>13,.2f}")
    print("=" * 58 + "\n")

    return grand_total



#  FILE I/O  –  Save to CSV
def save_to_csv(rows: list[dict], grand_total: float) -> None:
    """
    Write the portfolio summary to a CSV file.

    File I/O uses Python's built-in `csv` module.  The file is
    opened with newline='' (required on Windows) and encoding='utf-8'.

    Args:
        rows:        Per-stock data rows.
        grand_total: Total portfolio investment value.
    """
    fieldnames = ["Stock", "Quantity", "Price (USD)", "Total Value (USD)"]

    # 'w' mode creates the file if it doesn't exist, overwrites if it does
    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write a row for each stock holding
        for row in rows:
            writer.writerow({
                "Stock":             row["ticker"],
                "Quantity":          row["quantity"],
                "Price (USD)":       f"{row['price']:.2f}",
                "Total Value (USD)": f"{row['total_value']:.2f}",
            })

        # Append a separator and grand-total row at the bottom
        writer.writerow({})   # blank row for readability
        writer.writerow({
            "Stock":             "GRAND TOTAL",
            "Quantity":          "",
            "Price (USD)":       "",
            "Total Value (USD)": f"{grand_total:.2f}",
        })

    # Confirm success to the user
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"  💾  Portfolio saved to '{OUTPUT_CSV}'  [{timestamp}]")


#  ENTRY POINT
def main() -> None:
    """Main orchestration function."""

    # Step 1 – Collect the user's holdings via interactive loop
    portfolio = build_portfolio()

    # Guard: nothing was entered
    if not portfolio:
        print("\n  ℹ️  No stocks were added. Goodbye!\n")
        return

    # Step 2 – Calculate per-stock and total values
    rows = calculate_portfolio_value(portfolio)

    # Step 3 – Display the summary table in the console
    grand_total = print_summary(rows)

    # Step 4 – Persist the results to a CSV file (file I/O)
    save_to_csv(rows, grand_total)

    print("  Thank you for using the Stock Portfolio Tracker! 🚀\n")


if __name__ == "__main__":
    main()
