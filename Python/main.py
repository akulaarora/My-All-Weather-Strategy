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
    assets = None

    # Parse JSON into variables
    with open(STRATEGY, 'r') as f:
        strategy_json = json.loads(f.read())
        strategy_name = strategy_json['Name']
        band_threshold = strategy_json['Percent Band Threshold']
        assets = strategy_json['Portfolio']
        
    # Remove all invalid assets (no allocation or no ticker).
    # Converts to dictionary of asset names.
    temp = {}
    for asset in assets:
        if asset['Ticker'] != '' and asset['Percent Allocation'] != 0:
            name = asset.pop('Name')
            temp[name] = asset
    assets = temp

    # Get performance for all assets.
    assets = get_asset_changes(assets)

    # Push asset's performance to database
    for name in assets.keys():
        asset = assets[name]
        ticker = asset['Ticker']
        fields = {'Price': asset['Price'], 'Percent Change': asset['Percent Change']}
        db.write_asset_price(name, ticker, fields)

    # Updates portfolio
    balances, balanced = update_portfolio(strategy_name, assets, band_threshold)

    # Writes updated portfolio balances
    db.write_balance(strategy_name, balances, balanced=balanced)

def get_asset_changes(assets):
    """
    Calculate price changes on all assets
    Returns dict {asset -> 
        {"price" -> price, "Percent Change" -> percent_change, ... (from original)} }
    Mutates assets. Returns assets as well for ease of use.
    """
    for name in assets.keys():
        asset = assets[name]
        ticker = asset['Ticker']
        price = get_price_curr(ticker)

        prev_price = db.get_price_prev(ticker)
        if prev_price == None:
            percent_change = 0
            logging.error("Could not pull value for ticker " + ticker + " from database")
        else:
            percent_change = (price - prev_price) / prev_price * 100

        asset['Price'] = price
        asset['Percent Change'] = percent_change

    return assets


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


def update_portfolio(strategy_name, assets, band_threshold):
    """
    Handles all processing required to update the portfolio.
    Returns back the balances for the updated portfolio
    and whether the portfolio was created or rebalanced (balanced).
    As a tuple.
    """
    old = db.get_balance_prev(strategy_name)
    new = {}
    balanced = False

    if old == None:
        new = create_portfolio(assets)
        balanced = True
    else:
        total_balance = 0
        for name in old.keys():
            if name != 'Balance':
                balance = old[name]
                change = assets[name]['Percent Change'] / 100
                new_balance = balance * (1 + change)
                new[name] = new_balance
                total_balance += new_balance
        new['Balance'] = total_balance

        balanced = rebalance_portfolio(new, assets, band_threshold)

    return (new, balanced)

def create_portfolio(assets, size = 1.0):
    # Checks that portfolio allocation sums to 100%.
    sum = 0
    for name in assets.keys():
        allocation = assets[name]['Percent Allocation']
        sum += allocation
    if sum != 100:
        raise ValueError("Portfolio allocation does not sum to 100%")

    portfolio = {}
    portfolio['Balance'] = size
    for name in assets.keys():
        allocation = (assets[name]['Percent Allocation']) / 100
        portfolio[name] = size * allocation
    
    return portfolio


def rebalance_portfolio(portfolio, assets, band_threshold):
    rebalanced = False
    total_balance = portfolio['Balance']
    for name in portfolio.keys():
        if name != 'Balance':
            asset_balance = portfolio[name]
            allocation = assets[name]['Percent Allocation']
            curr_allocation  = asset_balance/total_balance * 100
            if abs(curr_allocation - allocation) >= band_threshold:
                create_portfolio(assets, size = total_balance)
                rebalanced = True
                break
    
    return rebalanced


if __name__ == "__main__":
    try:
        logging.basicConfig(filename=LOG, level=logging.DEBUG, \
            format='%(asctime)s %(levelname)s %(name)s %(message)s')

        main(sys.argv[1:])
    except Exception as e:
        logging.error(e)