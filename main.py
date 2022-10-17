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
    isStock = False if sp.find_all(class_="cart_tdc_sbn")[0].find("img") is not None else True
    print(title, isStock)
    return title, isStock

while(True):
    # 設定値読み込み
    with open("./config.json", "r") as f:
        conf = json.loads(f.read())

    # 在庫チェック&メッセージ作成
    msg = "\n"
    for store in conf["stores"]:
        for url in store["item_list"]:
            # 在庫チェック
            try:
                title,stock =  check_stock_akiduki(url)
                if stock:
                    msg = msg + f"{title}\n{url}\n"
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

