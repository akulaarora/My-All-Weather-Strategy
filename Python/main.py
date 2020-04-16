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
logger = None



def main(argv):
    # Get values from JSON file
    strategy_name = None
    portfolio_json = None
    band_threshold = None
    tickers = []

    with open(STRATEGY, 'r') as f:
        strategy_json = json.loads(f)
        portfolio_json = strategy_json['Portfolio']
        strategy_name = strategy_json["Name"]
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
        today_price = get_today_price(ticker)
        try:
            prev_price = get_prev_price(ticker)
            change_price = (today_price - prev_price) / prev_price * 100
        except Exception as e: # If I haven't already put in the data. Bad practice I know.
            change_price = 0
            logger.error("Could not pull value for ticker " + ticker + "from database")
        info = {"value": change_price, "Percent Change": change_price}
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

def get_current_portfolio():
    search = "SELECT value FROM balance WHERE ticker = " + ticker \
        + "GROUP BY * ORDER BY ASC LIMIT 1"
    client = InfluxDBClient('localhost', 8086, 'root', 'root', DATABASE_NAME)
    latest = client.query(search)

def update_portfolio(curr, ticker_performance):


def write_balance(strategy_name, fields):
    """
    Write balance to database.
    """
    data_point = [
        {
            "measurement": "balance",
            "tags": {
                "strategy": strategy_name
            },
            "fields": fields
        }
    ]

    write_point(data_point)

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
        logger = logging.basicConfig(filename=LOG, level=logging.DEBUG, 
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
        main(sys.argv[1:])
    except Exception as e:
        logger.error(e)