# Using BeautifulSoup to combine tables

import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time


def meta_data(month, year):

    with open("html_data/{}/{}.html".format(year, month), "rb") as html_file:
        soup = BeautifulSoup(html_file, "lxml")

    table = soup.find("table", {"class": "medias mensuales numspan"})

    # Pulling and creating whole data into the list
    try:

        # Pulling and creating rows of the table
        rows = [row.text for row in table.tr]

        texts = []
        for table in soup.find_all("table", {"class": "medias mensuales numspan"}):
            for tbody in table:
                for tr in tbody:
                    te = tr.get_text()
                    texts.append(te)

        numberOf_rows = round(len(texts) / len(rows))
        data = []
        for i in range(numberOf_rows):
            x = []
            for j in range(len(rows)):
                x.append(texts[j])
            data.append(x)
            del texts[:len(rows)]

        # Drop the unnecessary rows
        data.pop(0)
        data.pop(-1)

        df = pd.DataFrame(data, columns=rows)
        df.set_index("Day", inplace=True)
        df["Date"] = None
        for i in range(len(df)):
            df["Date"][i] = str(year) + "-" + str(month)

        df.replace(["", "-", " ", "o"], np.nan, inplace=True)

        return df.to_csv("data/{}-{}.csv".format(month, year))

    except Exception as e:
        print("{}-{} is not created. And there error is: {} ".format(month, year, e))


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

    for year in [2020]:
        for month in range(1, 10):
            new_df = pd.concat([new_df, combined_dataframe(month, year)], ignore_index=True)

    new_df.to_csv("combined_data_deneme.csv")
    print("Process Time: ", time.process_time() - start)