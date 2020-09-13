# Portfolio Manager

## Summary
This is a personal project to develop a portfolio management engine, allowing for implementation of new algorithmic trading strategies and portfolio rebalancing features. 

Notable features this project includes are:
- [TD Ameritrade Developers API](https://developer.tdameritrade.com/apis)
- Alex Golec's [`tda-api`](https://github.com/alexgolec/tda-api) wrapping that provides a very useful and clean way to interface with the TD Ameritrade API
- [Backtrader](https://github.com/mementum/backtrader), a Python package that enables users to easily back test their strategy prior to implementing them in production

## Motivation
I had more recently gotten serious about developing a good foundation in programming, system design, and overall just creating a product that wasn't just for looks but could actually provide value to myself. After discovering the TD Ameritrade API, I thought it would be a really cool opportunity to merge the two skills I was really interested in building: Data Science and Software Development

With the rise of roboadvisors and decline in active management, I thought I would personally try my hand at low(er) risk, algorithmic trading. My goals for this project are as follows:

1. Implement a portfolio rebalancing feature
2. Implement a simple algorithmic trading strategy
3. Implement a backtesting pipeline for new strategies
4. Implement a strategy ranking system that will auto-allocate portions of my portfolio to specific strategies

Though it's not hard to produce a strategy that makes money in the long run, it is very difficult to produce a "winning" strategy that outperforms the market consistently. My hope is that this repository will provide a foundation to set-up a local database structure and a structure to develop, test, and implement new strategies.

## Project Structure

```
[WIP] - Work in progress
[BETA] - Works in concept and could technically be run but should be refined

portfolio-manager
|
+-- account [WIP]
+-- portfolio
|   +-- __init__.py
|   +-- rebalance.py
|   +-- update_count.py [TO BE DELETED]
|
+-- scrap_work (This is where I keep my intermediary Jupyter Notebooks for prototyping and developing)
+-- setup
|   +-- setup_database.sql
|   +-- pop_securities.csv
|
+-- strategy
|   +-- production_strategy.py [BETA]
|   +-- backtest_strategy.py
|
+-- tests (Unit tests mirroring directory structure)
```

### account [WIP]
If this trading set-up were to manage multiple accounts, packages and scripts relevant to setting up new accounts, tracking balances, and updating gains overtime will be located in this folder.

### portfolio
Contains script to rebalance portfolio be extracting information from the local database and POSTing buy/sell orders to TDAmeritrade via the TDA-API.

### setup
Contains SQL script to set-up a PostgreSQL runtime database on the local machine and pre-populates the table with a pre-selected population of ETFs.

### strategy
Contains a file with all trading strategies and a file with the equivalent strategies to be backtested. These strategies are intended to be backtested regularly on the most recent TTM price data and algorithmically select the strategy that has performed the best to be used for the next rebalancing period.
