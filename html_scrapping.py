"""Air Quality in Istanbul between 2013 and 2019"""

import os
import time
import requests
import sys
import bs4
import sklearn

# ------------------- Data Collection Process -------------------
# Retrieving html from specific url

def retrieve_html():
    for year in range(2013, 2020):
        for month in range(1, 13):
            if month < 10:
                url = 'https://en.tutiempo.net/climate/0{}-{}/ws-170600.html'.format(month, year)
            else:
                url = 'https://en.tutiempo.net/climate/{}-{}/ws-170600.html'.format(month, year)

            data = requests.get(url)
            data_utf = data.text.encode('utf=8')

            if not os.path.exists("html_data/{}".format(year)):
                os.makedirs(("html_data/{}".format(year)))

            with open("html_data/{}/{}.html".format(year, month), "wb") as output:
                output.write(data_utf)

        sys.stdout.flush()


if __name__ == "__main__":
    start = time.process_time()
    retrieve_html()
    print("Process Time: ", (time.process_time() - start))
