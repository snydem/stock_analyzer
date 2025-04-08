import random
import pandas as pd

from typing import Tuple, Dict


def generate_random_data(stocks: int, weeks: int, stock_min: float,
                         stock_max: float, per_min: float,
                         per_max: float) -> Tuple[pd.Dataframe, Dict]:
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


def get_stock_data(*ticker_list, start, end):
    # Move Start and end to the nearest Monday and Friday respectively
    adjusted_start = move_to_monday() # Market Open
    adjusted_end = move_to_friday() # Market Close
    # Get the number of weeks between these two dates
    weeks = number_of_weeks(adjusted_start, adjusted_end)

    # loop through the ticker list and for each ticker
    for ticker in ticker_list:
        # loop through the weeks between the start and end date
        for week in range(weeks):
            # Get the percent change in the stock between market open and close
            # for the whole week. I.E. Market open on Monday and market close
            # on Friday.
            pass
        pass
    pass
