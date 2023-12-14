from entsoe import EntsoePandasClient
import pandas as pd
from dotenv import load_dotenv
import os

"""
    Method that can scrape information from market areas
    in a country.

    Args:
        func: The fucntion from the ENTSO-e API to call.
        type: What data is scraped.
        country: The country code used.
        areas: The index of the areas scraped. For single area countries
        this field can be an empty list.
        start: The start time.
        end: The end time.
"""
def get_from_areas(func, type, country, areas, start, end):
    if len(areas) < 1:
        df = pd.DataFrame({country + "_" + type: func(country, start=start, end=end)})
    else:
        df = pd.concat(
            [func(country + "_" + str(i), start=start, end=end) for i in areas], axis=1
        )
        df.columns = df.columns.astype(str)
        for i in range(0, len(areas)):
            df.columns.values[i] = country + str(i + 1) + "_" + type
return df

def load_forecasts(client, country, areas, start, end):
    return get_from_areas(client.query_load_forecast, "load",
                          country, areas, start, end)
