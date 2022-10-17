#-*- coding: utf-8 -*-
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import time

def send_line_message(token,message):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token,
    }
    files = {
        "message": (None, message),
    }
    res = requests.post(url, headers=headers, files=files)
    return res

def send_slack_message(token,channel,message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": "Bearer " + token,
    }
    data = {
        "channel": channel,
        "text": message
    }
    res = requests.post(url, headers=headers, data=data)
    return res

def check_stock_akiduki(url):
    sp = BeautifulSoup(requests.get(url).text, "html.parser")
    title = sp.find("title").text.split(":")[0]
    stock = sp.find_all(class_="cart_tdc_sbn")[0].find("img")
    stock = True if stock is None else False
    print(title, stock)
    return title, stock

def check_stock_switchscience(url):
    sp = BeautifulSoup(requests.get(url).text, "html.parser")
    title = sp.find("title").text
    stock = sp.find_all(class_="product-details__block")[7].text.replace("\n","").split(": ")[1]
    stock = stock if stock != "0" else False
    print(title, stock)
    return title, stock

while(True):
    # 設定値読み込み
    with open("./config.json", "r") as f:
        conf = json.loads(f.read())

    # 在庫チェック&メッセージ作成
    msg = ""
    for store in conf["stores"]:
        for url in store["item_list"]:
            # 在庫チェック
            try:
                if store["store_name"] == "akiduki":
                    title,stocks =  check_stock_akiduki(url)
                elif store["store_name"] == "switchscience":
                    title,stocks = check_stock_switchscience(url)
                if stocks:
                    msg = msg + f"\n{title}\nstock:{stocks}\n{url}"
            except KeyError as e:
                print(f"failed:Key {e} is not found.")
            except Exception as e:
                print(f"failed:{e}")

    # メッセージ送信
    if len(msg) != 0:
        ret = send_line_message(conf["line_token"],msg)
        print(f"line notifier response:{ret}")
        ret = send_slack_message(conf["slack_token"],conf["slack_channel"],msg)
        print(f"slack notifier response:{ret}")

    time.sleep(conf["interval"])

