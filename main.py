from flask import Flask, request
import datetime
import requests
from lunarcalendar import Converter, Solar
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

LINE_TOKEN = os.getenv("LINE_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

def is_two_days_before_lunar_1_or_15():
    target_date = datetime.date.today() + datetime.timedelta(days=2)
    solar = Solar(target_date.year, target_date.month, target_date.day)
    lunar = Converter.Solar2Lunar(solar)
    return lunar.day == 1 or lunar.day == 15

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
    r = requests.post(url, headers=headers, json=payload)
    print("訊息發送結果：", r.status_code, r.text)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

@app.route("/run", methods=["GET"])
def run():
    if is_two_days_before_lunar_1_or_15():
        send_message("提醒：後天是農曆初一或十五，記得買水果！🍇🍈🍉🍊🍌🍅🍓🍒🍑🍐🍏🍎🥭🥝🥑")
    return "Checked."

if __name__ == "__main__":
    app.run()
