#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def check_stock_akiduki(url):
    sp = BeautifulSoup(requests.get(url).text, "html.parser")
    title = sp.find("title").text.split(":")[0]
    isStock = False if sp.find_all(class_="cart_tdc_sbn")[0].find("img") is not None else True
    return title, isStock


url = "https://akizukidenshi.com/catalog/g/gM-16834/"
print(check_stock_akiduki(url))

url = "https://akizukidenshi.com/catalog/g/gM-13641/"
print(check_stock_akiduki(url))
