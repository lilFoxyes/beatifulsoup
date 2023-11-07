import pandas as pd
import requests 
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 (KHTML, like Gecko)"
    "Chrome/70.0.3538.77 Safari/537.36"
}

url = "https://finance.yahoo.com/quote/JDEP.AS/history?p=JDEP.AS"

response = requests.get(url, headers=headers)

if response.status_code != 200:
    raise Exception("Erro no request")

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", {"data-test": "historical-prices"})

