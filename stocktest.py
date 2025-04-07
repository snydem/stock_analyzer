import random
import pandas as pd
import copy
import csv


# Define number of weeks to run
WEEKS = 16
STOCKS = 4
# Starting Buying power in USD
INIT_BUYINGP = 1000
AMOUNT_PER_STOCK = (INIT_BUYINGP/2)//STOCKS
# Define Stock price mins and max
STOCK_MIN = 5
STOCK_MAX = 50
# Define possible percentatge swings min and max
PER_MIN = 0.5
PER_MAX = 1.5


def print_portfolio(portfolio):
    for k, v in portfolio.items():
        if k == "BP":
            print(k, v, sep='\t')
        else:
            print(k)
            print(f"\tSHARES: {v["SHARES"]}")
            print(f"\tEQUITY: {v["EQUITY"]}")
            print(f"\tPRICE PER SHARE: {v["PRICE_SHARE"]}")


def print_sim_results(sim_results):
    for week, portfolio in sim_results.items():
        print(f"============ WEEK {week} ============")
        print_portfolio(portfolio)


def stats_results(sim_results):
    week0 = sim_results[0]
    weekn = sim_results[WEEKS-1]
    total_final_equity = 0
    for stock, values in weekn.items():
        if stock != "BP":
            total_final_equity += values["EQUITY"]

    return total_final_equity


def results_to_csv(sim_results):
    with open("Results.csv", "w", newline='') as csvfile:
        fieldnames = ["Week", "TotalEquity"]
        fieldnames += [x for x in sim_results[0].keys()]
        writer = csv.writer(csvfile)
        for week, portfolio in sim_results.items():
            total_equity = 0
            stock_values = []
            for stock, values in portfolio.items():
                if stock != "BP":
                    stock_values.append(values["EQUITY"])
                    total_equity += values["EQUITY"]
            data = [week, total_equity] + stock_values
            writer.writerow(data)


# make list of random increases and decreases for each stock
percent_dict = {}
price_dict = {}
for i in range(STOCKS):
    # Generate Random Stock name
    name = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    percent_changes = []
    base_price = round(random.uniform(STOCK_MIN, STOCK_MAX), 2)
    for j in range(WEEKS):
        percent_changes.append(round(random.uniform(PER_MIN, PER_MAX), 2))
    percent_dict[name] = percent_changes
    price_dict[name] = base_price

percent_dataframe = pd.DataFrame(percent_dict)
portfolio = {
    "WEEK": [],
    "BUYING POWER": [],
    "STOCK": [],
    "SHARES": [],
    "PRICE PER SHARE": [],
    "EQUITY": []
}

# Start by buying all the necessary amounts of stocks
buying_power = INIT_BUYINGP
for stock, init_val in price_dict.items():
    shares_to_buy = AMOUNT_PER_STOCK/init_val
    buying_power -= AMOUNT_PER_STOCK
    portfolio["WEEK"].append(0)
    portfolio["BUYING POWER"].append(buying_power)
    portfolio["STOCK"].append(stock)
    portfolio["SHARES"].append(shares_to_buy)
    portfolio["PRICE PER SHARE"].append(init_val)
    portfolio["EQUITY"].append(AMOUNT_PER_STOCK)

port_df = pd.DataFrame(portfolio)
portfolio_by_week = {0: copy.deepcopy(portfolio)}

# Each row is a week step in the simulation
for index, row in percent_dataframe.iterrows():
    week = index + 1
    for stock in percent_dataframe:
        # Get the number of shares of stock you will buy
        per_change = row[stock]
        last_row = \
            port_df[(port_df["STOCK"] == stock) & (port_df["WEEK"] == week-1)]
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
                week, buying_power, stock, new_shares, new_price, new_equity]

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
                week, buying_power, stock, new_shares, new_price, new_equity]

print(port_df)
starting_eq = port_df[port_df["WEEK"] == 0]
ending_eq = port_df[port_df["WEEK"] == WEEKS]
starting_eq = starting_eq["EQUITY"].sum()
ending_eq = ending_eq["EQUITY"].sum()
print(starting_eq, ending_eq)
