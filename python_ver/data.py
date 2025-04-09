import random
import requests
import json
import datetime
import pandas as pd

from typing import Tuple, Dict

# REMOVE THIS BEFORE A PUSH
api_key = "2JO3H0UB2DDQS0E2"


def generate_random_data(stocks: int, weeks: int, stock_min: float,
                         stock_max: float, per_min: float,
                         per_max: float) -> Tuple[pd.DataFrame, Dict]:
    """
    Generate random stock data for the goal and purpose of testing the stock
    simulation.
    """
    percent_dict = {}
    price_dict = {}
    for i in range(stocks):
        # Generate Random Stock name
        name = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
        percent_changes = []
        base_price = round(random.uniform(stock_min, stock_max), 2)
        for j in range(weeks):
            percent_changes.append(round(random.uniform(per_min, per_max), 2))
        percent_dict[name] = percent_changes
        price_dict[name] = base_price

    percent_dataframe = pd.DataFrame(percent_dict)
    return percent_dataframe, price_dict


def _next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def stock_weekly_data(symbol):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY" \
          f"&symbol={symbol}&apikey={api_key}"
    r = requests.get(url)
    data = r.json()
    return data


def get_stock_data(*ticker_list, start_date, num_weeks):
    # Move Start and end to the nearest Monday and Friday respectively
    adjusted_start =  datetime.datetime(start_date) # Market Open date

    # loop through the ticker list and for each ticker
    for ticker in ticker_list:
        stock_date = _next_weekday(0, adjusted_start)
        stock_data = stock_weekly_data(ticker)
        # loop through the weeks between the start and end date
        for week in range(num_weeks):
            # Get the percent change in the stock between market open and close
            # for the whole week. I.E. Market open on Monday and market close
            # on Friday.
            open_price = None
            close_price = None
            try:
                open_price = float(stock_data["Weekly Time Series"]["1. open"])
                # Move to friday:
                stock_date = stock_date + datetime.timedelta(4)
                close_price = float(stock_data["Weekly Time Series"]["4. close"])
                # Move to monday:
                stock_date = stock_date + datetime.timedelta(3)
            except KeyError:
                Exception("NUM WEEKS EXTENDS PAST CURRENT AVAILABLE DATA")
            # Calculate the percentage change over this week
            percent_change = (close_price - open_price)/open_price
            print(percent_change)
        pass
    pass


if __name__ == '__main__':
    stock_weekly_data(symbol="IBM")
    get_stock_data(["IBM"], start_date="03-31-2025", num_weeks=1)

