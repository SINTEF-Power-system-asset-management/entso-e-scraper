# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

from entsoe import EntsoePandasClient

import pandas as pd

from dotenv import load_dotenv
import os

start = pd.Timestamp('20230806', tz='Europe/Brussels')
end = pd.Timestamp('20230807', tz='Europe/Brussels')

load_dotenv()

api_key = os.environ.get('api_key')

client = EntsoePandasClient(api_key=api_key)


def get_from_areas(func, type, country, areas, start, end):
    if len(areas) < 1:
        df = pd.DataFrame({country+"_"+type: func(country, start=start, end=end)})
    else:
        df = pd.concat(
            [func(country+"_"+str(i), start=start, end=end) for i in areas], axis=1)
        df.columns = df.columns.astype(str)
        for i in range(0, len(areas)):
            df.columns.values[i] = country+str(i+1)+"_"+type
    return df


def load_forecasts(client, country, areas, start, end):
    return get_from_areas(client.query_load_forecast, "load",
                          country, areas, start, end)


def price_forecasts(client, country, areas, start, end):
    return get_from_areas(client.query_day_ahead_prices, "price",
                          country, areas, start, end)


loads = load_forecasts(client, "NO", range(1,6), start, end)

loads.plot()



cb_list = [("SE_3", "NO_1"), ("SE_2", "NO_3"),
           ("SE_2", "NO_4"), ("SE_1", "NO_4"),
           ("FI", "NO_4")]

FI_prices = price_forecasts(client, "FI", [], start, end)
SE_prices = price_forecasts(client, "SE", range(1, 4), start, end)
NO_prices = price_forecasts(client, "NO", range(1,6), start, end)
DK_prices = price_forecasts(client, "DK", range(1,3), start, end)
DE_prices = price_forecasts(client, "DE_LU", [], start, end)
NSL_prices = price_forecasts(client, "NO_2_NSL", [], start, end)

prices = pd.concat([NO_prices, DK_prices, SE_prices, FI_prices, DE_prices, NSL_prices], axis=1)

prices.plot()

prices.to_csv("prices-2023-08-06_2023-08-07.csv")
loads.to_csv("loads-2023-08-06_2023-08-07.csv")

cross_border = pd.DataFrame(
    [client.query_crossborder_flows(cb[0], cb[1], start=start, end=end) for cb in cb_list])

cross_border.T.plot()

cross_border.T


