# Akul's All Weather Strategy Implementation (Quick Design Doc)

## Links
[Whitepaper](https://www.bridgewater.com/resources/all-weather-story.pdf)

[Portfolio Visualizer](https://www.portfoliovisualizer.com/backtest-asset-class-allocation?s=y&mode=1&timePeriod=4&startYear=1972&firstMonth=1&endYear=2020&lastMonth=12&calendarAligned=true&includeYTD=false&initialAmount=10000&annualOperation=0&annualAdjustment=0&inflationAdjusted=true&annualPercentage=0.0&frequency=4&rebalanceType=5&absoluteDeviation=5.0&relativeDeviation=25.0&benchmark=VBINX&portfolioNames=false&portfolioName1=Ray+Dalio+All+Weather&portfolioName2=Ray+Dalio+All+Weather&portfolioName3=Portfolio+3&asset1=TotalStockMarket&allocation1_1=0&allocation1_2=30&asset2=LongTreasury&allocation2_1=40&allocation2_2=40&asset3=IntermediateTreasury&allocation3_1=15&allocation3_2=15&asset4=Commodities&allocation4_1=0&allocation4_2=7.5&asset5=Gold&allocation5_1=15&allocation5_2=7.5&asset6=SmallCapBlend&allocation6_1=15&asset7=LargeCapBlend&allocation7_1=10&asset8=REIT&allocation8_1=5)

[Portfolio Visualizer (Long-term; substituted some of the asset classes)](https://www.portfoliovisualizer.com/backtest-asset-class-allocation?s=y&mode=1&timePeriod=4&startYear=1972&firstMonth=1&endYear=2020&lastMonth=12&calendarAligned=true&includeYTD=false&initialAmount=10000&annualOperation=0&annualAdjustment=0&inflationAdjusted=true&annualPercentage=0.0&frequency=4&rebalanceType=5&absoluteDeviation=5.0&relativeDeviation=25.0&benchmark=VBINX&portfolioNames=false&portfolioName1=Ray+Dalio+All+Weather&portfolioName2=Ray+Dalio+All+Weather&portfolioName3=Portfolio+3&asset1=TotalStockMarket&allocation1_1=0&allocation1_2=30&asset2=LongTreasury&allocation2_1=40&allocation2_2=40&asset3=IntermediateTreasury&allocation3_1=15&allocation3_2=15&asset4=Commodities&allocation4_1=7.5&allocation4_2=7.5&asset5=Gold&allocation5_1=7.5&allocation5_2=7.5&asset6=SmallCapBlend&allocation6_1=15&asset7=LargeCapBlend&allocation7_1=10&asset8=REIT&allocation8_1=5)


## How to deploy this
### Prerequisites
- Docker and docker-compose

### Steps
1. Pull this repository.
2. Create a folder in Python called DONOTPUSH with file api_keys.py. Add AV_KEY="\<YOUR ALPHAVANTAGE KEY\>".
2. Set up a cronjob to run this. See example crontab provided.
3. Use docker compose to set up the containers.
  - This will also run on the first crontab iteration, so this is not totally necessary. You can use this to test and ensure everything works as it should.


## How this Works
Deployed in Docker container on Microsoft Azure server:

TODO: Will create a web server to show output. Right now, I am just storing to the database.

## Docker environment
Python script that is the brains of the strategy. Does the following:
1. Pulls any changes to set up from Github repository.
2. Pulls financial data.
3. Computes how the portfolio would have performed that day.
4. Handles any rebalancing of portfolio to achieve set allocation.
5. Pushes latest data to database.
6. Updates website. TODO

JSON file that contains the strategy (allocations and how to rebalance).

InfluxDB database that stores timeseries data of how the strategy performed each day.

File containing API keys.
- Untracked from Git, so I don't accidentally my logins public.

### Cronjob manager
Cron job manages docker environment. Runs script every weekday at 2pm PST (one hour after market close to get data for the day).
1. Will pull the latest changes from git.
2. Starts Docker
3. Runs environment to get data.
4. Shuts down environment and turns off docker.

## InfluxDB inforomation stored
Time, current balance, balance of each asset in portfolio, stock price of each asset in portfolio
- Current balance is from a starting amount of $1 in the database.
- Measurements: price -> stock prices; balance -> asset balance

## Web server
TODO

## Services used
Alphavantage - financial data

Docker - container

Azure - hosting server
Github - website hosting

## Further work
Step 1 of Python script. It would be nice if I can make a change and it automatically updates.
- Cannot figure out how to pull in Python. Alternative is to add a bash script that runs with login info.

Only run cron job on weekdays that market is open (ignore holidays).

Check for stock splits.

Store more data to server than just the performance of the portfolio.
- Individual stocks performance

Display more information on the webpage.

## Notes
This is a rough project that I put together for fun. Don't treat this as a representation of what production-level/industry work I do is like.
