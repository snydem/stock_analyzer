import random
import pandas as pd
import copy
import csv

# TODO: Either add these as commandline args or in an ini file
# Define number of weeks to run
WEEKS = 32
STOCKS = 100
# Starting Buying power in USD
INIT_BUYINGP = 1000
AMOUNT_PER_STOCK = (INIT_BUYINGP/2)//STOCKS
# Define Stock price mins and max
STOCK_MIN = 5
STOCK_MAX = 50
# Define possible percentatge swings min and max
PER_MIN = 0.5
PER_MAX = 1.5


def simulation_1(percent_dataframe, port_df):
    buying_power = INIT_BUYINGP
    for index, row in percent_dataframe.iterrows():
        week = index + 1
        for stock in percent_dataframe:
            # Get the number of shares of stock you will buy
            per_change = row[stock]
            last_row = port_df[
                (port_df["STOCK"] == stock) & (port_df["WEEK"] == week-1)]
            current_price = list(last_row["PRICE PER SHARE"])[0]
            current_shares = list(last_row["SHARES"])[0]
            new_price = round(current_price * per_change, 2)

            if new_price > current_price:
                # Sell if we gained money
                usd_to_sell = round((per_change - 1) * 100, 2)
                shares_to_sell = usd_to_sell/new_price
                if shares_to_sell > current_shares:
                    new_equity = current_shares * new_price
                    port_df.loc[len(port_df)] = [week, buying_power, stock,
                                                 current_shares, new_price,
                                                 new_equity]
                    continue

                # update the portfolio
                new_shares = current_shares - shares_to_sell
                new_equity = new_shares * new_price
                buying_power += usd_to_sell
                port_df.loc[len(port_df)] = [
                    week, buying_power, stock, new_shares, new_price,
                    new_equity]

            else:
                # Buy if we lost value
                usd_to_buy = round((per_change) * 100, 2)
                shares_to_buy = usd_to_buy/new_price
                if usd_to_buy > buying_power:
                    # if we need to buy more than we have, do not buy
                    new_equity = current_shares * new_price
                    port_df.loc[len(port_df)] = [week, buying_power, stock,
                                                 current_shares, new_price,
                                                 new_equity]
                    continue
                # update the portfolio
                new_shares = current_shares + shares_to_buy
                new_equity = new_shares * new_price
                buying_power -= usd_to_buy

                port_df.loc[len(port_df)] = [
                    week, buying_power, stock, new_shares, new_price,
                    new_equity]
