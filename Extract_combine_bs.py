# Using BeautifulSoup to combine tables


import requests
import sys
import os
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import matplotlib as plt

def met_data(month, year):

    with open("Data/{}/{}.html".format(year, month), "rb") as html_file:
        soup = BeautifulSoup(html_file, "lxml")

    # Pulling and creating Columns of the table
    table = soup.find("table", {"class":"medias mensuales numspan"})
    columns = [column.text for column in table.tr]

    # Pulling and creating whole data into the list
    try:
        texts = []
        for table in soup.find_all("table", {"class": "medias mensuales numspan"}):
            for tbody in table:
                for tr in tbody:
                    texts.append(tr.text)

    except Exception as e:
        print("error")


    try:
        numberOf_rows = round(len(texts) / len(columns))
        data = []
        for i in range(numberOf_rows):
            x = []
            for j in range(len(columns)):
                x.append(texts[j])
            data.append(x)
            del texts[:len(columns)]

    except Exception as e:
        print("ok")

    data.pop(0)
    df = pd.DataFrame(data, columns=columns)
    df.set_index("Day", inplace=True)


    print(df.head(10))

met_data(5, 2015)
