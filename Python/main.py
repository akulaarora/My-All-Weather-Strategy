import sys
sys.path.append("../")
sys.path.append("DONOTPUSH/")

import api_keys

import json
from time import sleep
from github import Github
from influxdb import InfluxDBClient
from alpha_vantage.timeseries import TimeSeries

REPO_NAME = "My-All-Weather-Strategy"
DATABASE_NAME = "All_Weather"
STRATEGY = "../strategy.json"
LOG = "DONOTPUSH/errors.log"


def main(argv):
    # Get values from JSON file
    portfolio_json = None
    band_threshold = None
    tickers = []

    with open(STRATEGY, 'r') as f:
        portfolio_json = strategy_json['Portfolio']
        band_threshold = strategy_json['Percent Band Threshold']
        
    for asset in portfolio_json:
        if asset['Ticker'] != '':
            tickers.append(asset['Ticker'])

    # Get performance for all stocks and push to database
    ticker_performance = get_performance_today(tickers)
    for asset in portfolio_json:
        ticker = asset['Ticker']
        if ticker != '':
            write_stock_price(asset['Name'], ticker, ticker_performance[ticker])
        


def get_stock_changes(tickers):
    """
    Calculate price changes on all tickers
    """
    dict = {}
    for ticker in tickers:
        prev_price = get_prev_price(ticker)
        today_price = get_today_price(ticker)
        change_price = (today_price - prev_price) / prev_price * 100
        info = {"value": ticker, "Percent Change": change_price}
        dict[ticker] = info

    return dict

    def get_prev_price(ticker):
        """
        Pulls data from InfluxDB using list of tickers.
        Returns back previous close for ticker.
        """
        search = "SELECT value FROM price WHERE ticker = " + ticker \
            + "GROUP BY * ORDER BY ASC LIMIT 1"
        client = InfluxDBClient('localhost', 8086, 'root', 'root', DATABASE_NAME)
        price = client.query(search)

        return price

    def get_today_price(ticker):
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
            except ValueError as e:
                sleep(61)
                attempts += 1

def write_balance(data_type, na)
    """
    Write balance to database.
    """
    data_point = [
        {
            "measurement": "price",
            "tags": {
                "name": name,
                "ticker": ticker
            },
            "fields": {
                "Overall Balance": value
            }
        }
    ]

def write_stock_price(name, ticker, fields):
    """
    Writes stock price to database.
    """
    # TODO Might need to specify timestamp
    data_point = [
        {
            "measurement": "price",
            "tags": {
                "name": name,
                "ticker": ticker
            },
            "fields": fields
        }
    ]

    write_point(data_point)

def write_point(point):
    """
    Writes data point to database.
    Documentation used: http://influxdb-python.readthedocs.io/en/latest/include-readme.html#documentation
    Note: This is code I have copied from one of my other repositories (Caltran_traffic).
    """
    try:
        client = InfluxDBClient('localhost', 8086, 'root', 'root', DATABASE_NAME)
        client.create_database(DATABASE_NAME)  # Will create database if it does not exist. Otherwise, does not modify database.
        client.write_points(data_point, time_precision = 'h')
    except:
        raise error("Could not write data for {} due to error with InfluxDB database".format(identifier))

def update_contents():
    g = Github(api_keys.GH_KEY)
    repo = g.get_repo(REPO_NAME)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        logFile = open(LOGFILE)
        logFile.write(e)
        logFile.close()