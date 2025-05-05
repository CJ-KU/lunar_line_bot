from flask import Flask, request
import datetime
import requests
from lunarcalendar import Converter, Solar
from dotenv import load_dotenv
import os

# 載入環境變數（包含 LINE_TOKEN 與 GROUP_ID）
load_dotenv()

app = Flask(__name__)

LINE_TOKEN = os.getenv("LINE_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

def is_two_days_before_lunar_1_or_15():
    try:
        target_date = datetime.date.today() + datetime.timedelta(days=2)
        solar = Solar(target_date.year, target_date.month, target_date.day)
        converter = Converter()
        lunar = converter.Solar2Lunar(solar)
        return lunar.day == 1 or lunar.day == 15
    except Exception as e:
        print("判斷農曆日期時發生錯誤：", e)
        return False

def send_message(msg):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Authorization': f'Bearer {LINE_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'to': GROUP_ID,
        'messages': [{'type': 'text', 'text': msg}]
    }
    try:
        r = requests.post(url, headers=headers, json=payload)
        print("訊息發送結果：", r.status_code, r.text)
    except Exception as e:
        print("傳送 LINE 訊息失敗：", e)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

@app.route("/run", methods=["GET"])
def run():
    try:
        if is_two_days_before_lunar_1_or_15():
            send_message("提醒：後天是農曆初一或十五，記得買水果！🍇🍈🍉🍊🍌🍅🍓🍒🍑🍐🍏🍎🥭🥝🥑")
        return "Checked."
    except Exception as e:
        print("執行 /run 發生錯誤：", e)
        return f"Internal Server Error: {str(e)}", 500

if __name__ == "__main__":
    app.run()
