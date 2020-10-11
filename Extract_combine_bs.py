# Using BeautifulSoup to combine tables

from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import os
import numpy as np


def meta_data(month, year):
    with open("html_data/{}/{}.html".format(year, month), "rb") as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    table = soup.find("table", {"class": "medias mensuales numspan"})

    try:
        # Pulling the title of the columns
        cols = [col.text for col in table.tr]

        # Pulling the values on the table
        style = soup.select_one('.medias').find_previous('style').string
        mapper = dict(re.findall(r'([^.]+?)::after{content:"(.*?)"', style))
        for span in soup.find_all('span', class_=lambda cl: cl in mapper):
            span.replace_with(mapper[span['class'][0]])

        data = []
        for row in soup.select('.medias tr'):
            texts = [td.text for td in row.select('td') if td.text.strip()]
            data.append(texts[:11])

        # Creating Dataframe.
        df = pd.DataFrame(data[:-2], columns=cols[:11])
        df.set_index("Day", inplace=True)
        df["Date"] = None
        for i in range(len(df)):
            df["Date"][i] = str(year) + "-" + str(month)

        df.replace(["", "-", " ", "o"], np.nan, inplace=True)

        return df.to_csv("data/{}-{}.csv".format(month, year))

    except Exception as e:
        print("{}-{} is not created. And the error is: {} ".format(month, year, e))


def combined_dataframe(month, year):
    return pd.read_csv("data/{}-{}.csv".format(month, year))


if __name__ == "__main__":

    start = time.process_time()
    if not os.path.exists("data"):
        os.makedirs("data")

    for year in range(2014, 2020):
        for month in range(1, 13):
            meta_data(month, year)

    for year in [2020]:
        for month in range(1, 10):
            meta_data(month, year)

    new_df = pd.DataFrame(None)

    for year in range(2014, 2020):
        for month in range(1, 13):
            new_df = pd.concat([new_df, combined_dataframe(month, year)], ignore_index=True)

    # Due to 2020 year has only 9 months. We are in 19-11-2020
    for year in [2020]:
        for month in range(1, 10):
            new_df = pd.concat([new_df, combined_dataframe(month, year)], ignore_index=True)

    new_df.to_csv("combined_data_deneme.csv")
    print("Process Time: ", time.process_time() - start)
