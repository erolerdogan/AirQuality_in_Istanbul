# Using BeautifulSoup to combine tables

import sys
import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def meta_data(month, year):

    with open("html_data/{}/{}.html".format(year, month), "rb") as html_file:
        soup = BeautifulSoup(html_file, "lxml")

    table = soup.find("table", {"class": "medias mensuales numspan"})

    # Pulling and creating whole data into the list
    try:

        # Pulling and creating Columns of the table
        columns = [column.text for column in table.tr]

        texts = []
        for table in soup.find_all("table", {"class": "medias mensuales numspan"}):
            for tbody in table:
                for tr in tbody:
                    texts.append(tr.text)

        numberOf_rows = round(len(texts) / len(columns))
        data = []
        for i in range(numberOf_rows):
            x = []
            for j in range(len(columns)):
                x.append(texts[j])
            data.append(x)
            del texts[:len(columns)]

        # Drop the unnecessary rows

        data.pop(0)
        data.pop(-1)

        df = pd.DataFrame(data, columns=columns)
        df.set_index("Day", inplace=True)
        df.replace(["", "-", " ", "o"], np.nan, inplace=True)

        return df.to_csv("data/{}-{}.csv".format(month, year))

    except Exception as e:
        print("{}-{} is not created. ".format(month, year))


if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")

    for year in range(2013, 2020):
        for month in range(1, 13):
            meta_data(month, year)


