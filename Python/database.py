from influxdb import InfluxDBClient

DATABASE_ADDR = "influxdb-grafana"
DATABASE_PORT = 8086
DATABASE_NAME = "All_Weather"

# Connect to server
client = InfluxDBClient(DATABASE_ADDR, DATABASE_PORT, DATABASE_NAME)
client.create_database(DATABASE_NAME)

### GETTERS
def get_current_portfolio():
    search = "SELECT value FROM balance " \
        + "GROUP BY * ORDER BY ASC LIMIT 1"
    latest = client.query(search, DATABASE_NAME)



def get_price_prev(ticker):
    """
    Pulls data from InfluxDB using list of tickers.
    Returns back previous close for ticker.
    """
    search = "SELECT value FROM price WHERE ticker =\'" + ticker + "\'" \
        + " GROUP BY * ORDER BY ASC LIMIT 1"
    result = client.query(search, database=DATABASE_NAME)

    return next(result['price'])['value']


### SETTERS
def write_balance(strategy_name, fields):
    """
    Writes portfolio balance to database.
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
    Writes data point to database. Time precision is hour.
    Documentation used: http://influxdb-python.readthedocs.io/en/latest/include-readme.html#documentation
    Note: This is code I have copied from one of my other repositories (Caltran_traffic).
    """
    try:
        client.write_points(point, database=DATABASE_NAME, time_precision = 'h')
    except:
        raise RuntimeError("Could not write data for {} due to error with InfluxDB database".format(point))
    
