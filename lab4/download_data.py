import os
import requests
from zipfile import ZipFile
from datetime import datetime


def download_dataset():
    if not os.path.exists("data"):
        os.makedirs("data")    

    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError

    with open("./lab4/data/household_power_consumption.zip", 'wb') as file:
        for chunk in response:
            file.write(chunk)

    with ZipFile("./lab4/data/household_power_consumption.zip") as zipFile:
        zipFile.extractall("data")

if __name__ == "__main__":
    download_dataset()