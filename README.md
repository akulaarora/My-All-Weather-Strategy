# Akul's All Weather Strategy Implementation (Quick Design Doc)

## Links
[Whitepaper](https://www.bridgewater.com/resources/all-weather-story.pdf)
[Portfolio Visualizer](https://www.portfoliovisualizer.com/backtest-asset-class-allocation?s=y&mode=1&timePeriod=4&startYear=1972&firstMonth=1&endYear=2020&lastMonth=12&calendarAligned=true&includeYTD=false&initialAmount=10000&annualOperation=0&annualAdjustment=0&inflationAdjusted=true&annualPercentage=0.0&frequency=4&rebalanceType=5&absoluteDeviation=5.0&relativeDeviation=25.0&benchmark=VBINX&portfolioNames=false&portfolioName1=Ray+Dalio+All+Weather&portfolioName2=Ray+Dalio+All+Weather&portfolioName3=Portfolio+3&asset1=TotalStockMarket&allocation1_1=0&allocation1_2=30&asset2=LongTreasury&allocation2_1=40&allocation2_2=40&asset3=IntermediateTreasury&allocation3_1=15&allocation3_2=15&asset4=Commodities&allocation4_1=0&allocation4_2=7.5&asset5=Gold&allocation5_1=15&allocation5_2=7.5&asset6=SmallCapBlend&allocation6_1=15&asset7=LargeCapBlend&allocation7_1=10&asset8=REIT&allocation8_1=5)

[Portfolio Visualizer (Long-term; substituted some of the asset classes)](https://www.portfoliovisualizer.com/backtest-asset-class-allocation?s=y&mode=1&timePeriod=4&startYear=1972&firstMonth=1&endYear=2020&lastMonth=12&calendarAligned=true&includeYTD=false&initialAmount=10000&annualOperation=0&annualAdjustment=0&inflationAdjusted=true&annualPercentage=0.0&frequency=4&rebalanceType=5&absoluteDeviation=5.0&relativeDeviation=25.0&benchmark=VBINX&portfolioNames=false&portfolioName1=Ray+Dalio+All+Weather&portfolioName2=Ray+Dalio+All+Weather&portfolioName3=Portfolio+3&asset1=TotalStockMarket&allocation1_1=0&allocation1_2=30&asset2=LongTreasury&allocation2_1=40&allocation2_2=40&asset3=IntermediateTreasury&allocation3_1=15&allocation3_2=15&asset4=Commodities&allocation4_1=7.5&allocation4_2=7.5&asset5=Gold&allocation5_1=7.5&allocation5_2=7.5&asset6=SmallCapBlend&allocation6_1=15&asset7=LargeCapBlend&allocation7_1=10&asset8=REIT&allocation8_1=5)

## How this Runs
Deployed in Docker container on Microsoft Azure server

Hosted by Github.io pages

To update static Github page, Docker instance pushes a commit every day with the latest information.

## What is on the Docker container
Python script that is the brains of the strategy. Does the following:
1. Pulls any changes to set up from Github repository.
2. Pulls financial data.
3. Computes how the portfolio would have performed that day.
4. Handles any rebalancing of portfolio to achieve set allocation.
5. Pushes latest data to database.
6. Updates Github page and pushes to Git.

Cron job runs script every weekday at 2pm PST (one hour after market close to )

JSON file that contains the strategy (allocations and how to rebalance).

InfluxDB database that stores timeseries data of how the strategy performed each day.

File containing API keys.
- Untracked from Git, so I don't accidentally my logins public.

## InfluxDB inforomation stored
Time, current balance, balance of each asset in portfolio, stock price of each asset in portfolio
- Current balance is from a starting amount of $100,000.

## Github page
For now, just display the daily information from InfluxDB on the Github page.

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

Display more information on the Github page.
- Eventually, would be cool to make a dynamic layout that pulls information directly from database.
 - E.g. visualizations, performance over time periods etc.
 - This will most likely require a dynamic page (not Github pages).  

## Notes
This is a rough project that I put together for fun. Don't treat this as a representation of what production-level/industry work I do is like.