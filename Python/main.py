# For importing keys
import sys
sys.path.append("../")
sys.path.append("DONOTPUSH/")
import api_keys

# My modules
import database as db

# Libraries
import json
from time import sleep
# from github import Github
from alpha_vantage.timeseries import TimeSeries
import logging

# Constants
REPO_NAME = "My-All-Weather-Strategy"
STRATEGY = "../strategy.json"
LOG = "DONOTPUSH/errors.log"

# Global objects
client = None


def main(argv):
    # Get values from JSON file
    strategy_name = None
    portfolio_json = None
    band_threshold = None
    tickers = []

    # Parse JSON into variables
    with open(STRATEGY, 'r') as f:
        strategy_json = json.loads(f.read())
        portfolio_json = strategy_json['Portfolio']
        strategy_name = strategy_json['Name']
        band_threshold = strategy_json['Percent Band Threshold']
        
    # Get all valid tickers
    for asset in portfolio_json:
        if asset['Ticker'] != '':
            tickers.append(asset['Ticker'])

    # Get performance for all tickers. Stores to ticker_performance.
    ticker_performance = get_stock_changes(tickers)

    # Push stock's performance to database
    for asset in portfolio_json:
        ticker = asset['Ticker']
        if ticker != '':
            db.write_stock_price(asset['Name'], ticker, ticker_performance[ticker])

    # Get previous portfolio values.

    # Calculate portfolio improvement
    
    update_portfolio()

def get_stock_changes(tickers):
    """
    Calculate price changes on all tickers
    Returns dict ticker -> {"value" -> value, "Percent Change" -> percent_change}
    """
    stock_changes = {}
    for ticker in tickers:
        value = get_price_curr(ticker)
        try:
            prev_price = db.get_price_prev(ticker)
            percent_change = (value - prev_price) / prev_price * 100
        except Exception: # If I haven't already put in the data. Bad practice I know.
            percent_change = 0
            logging.error("Could not pull value for ticker " + ticker + " from database")
        info = {"value": value, "Percent Change": percent_change}
        stock_changes[ticker] = info

    return stock_changes


def get_price_curr(ticker):
    """
    Pulls data from Alphavantage using ticker.
    Returns back close for today (latest value).
    """
    ts = TimeSeries(api_keys.AV_KEY)
    attempts = 1
    while attempts <= 2:
        try:
            data = ts.get_quote_endpoint(symbol=ticker)
            price = float(data[0]['05. price'])
            return price
        except ValueError:
            sleep(61)
            attempts += 1


def update_portfolio(curr, ticker_performance):
    print()


# def update_contents():
    # g = Github(api_keys.GH_KEY)
    # repo = g.get_repo(REPO_NAME)


if __name__ == "__main__":
    # try:
    logging.basicConfig(filename=LOG, level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    main(sys.argv[1:])
# except Exception as e:
# logging.error(e)