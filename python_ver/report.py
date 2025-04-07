import csv


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
