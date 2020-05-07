from influxdb import InfluxDBClient

DATABASE_ADDR = "influxdb-grafana"
DATABASE_PORT = 8086
DATABASE_NAME = "All_Weather"

# Connect to server
client = InfluxDBClient(DATABASE_ADDR, DATABASE_PORT, DATABASE_NAME)
client.create_database(DATABASE_NAME)


def print_balances():
    result = client.query("SELECT * FROM balance", database=DATABASE_NAME)
    for line in result.get_points():
        print("Time: ", line['time'], "   Balance: ", line['Balance'])

### GETTERS
def get_balance_prev(strategy_name):
    """
    Gets the portfolio balance right now 
    (previous in the context of now being the current).
    Returns None if it could not be found.
    """
    search = "SELECT * FROM balance WHERE strategy=\'" \
        + strategy_name + "\'" \
        + " GROUP BY * ORDER BY ASC LIMIT 1"
    result = client.query(search, database=DATABASE_NAME)
    if result.keys() == []:
        return None

    ret = next(result['balance'])
    ret.pop('time')

    return ret


def get_price_prev(ticker):
    """
    Pulls data from InfluxDB using ticker.
    Returns back previous last price stored for ticker.
    If it could not find, returns back None.
    """
    search = "SELECT value FROM price WHERE ticker =\'" + ticker + "\'" \
        + " GROUP BY * ORDER BY ASC LIMIT 1"
    result = client.query(search, database=DATABASE_NAME)

    if result.keys() == []:
        return None

    return next(result['price'])['price']


### SETTERS
def write_balance(strategy_name, fields, balanced = False):
    """
    Writes portfolio balance to database.
    Balanced specifies if the portfolio was created or rebalanced.
    Balanced is a tag.
    """
    data_point = [
        {
            "measurement": "balance",
            "tags": {
                "strategy": strategy_name,
                "balanced": balanced
            },
            "fields": fields
        }
    ]

    write_point(data_point)


def write_asset_price(name, ticker, fields):
    """
    Writes asset price to database.
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
    
