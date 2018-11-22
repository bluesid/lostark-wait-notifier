# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
███████╗██╗   ██╗██╗████████╗███████╗   ██╗      █████╗ ██████╗
██╔════╝██║   ██║██║╚══██╔══╝██╔════╝   ██║     ██╔══██╗██╔══██╗
███████╗██║   ██║██║   ██║   █████╗     ██║     ███████║██████╔╝
╚════██║██║   ██║██║   ██║   ██╔══╝     ██║     ██╔══██║██╔══██╗
███████║╚██████╔╝██║   ██║   ███████╗██╗███████╗██║  ██║██████╔╝
╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚═════╝
═══════════════════════════════════════════════════════════════
                Lost Ark wait notifier api
                develop by woosik yoon (yoonwoosik12@naver.com)
                [suitee.me]
═══════════════════════════════════════════════════════════════
"""

from flask import Flask, request, jsonify
from dbtools import *
import datetime
from crawler import *

app = Flask(__name__)
db = DbTools(select_only=True)

@app.route('/keyboard')
def Keyboard():
    dataSend = {
        "type": "buttons",
        "buttons": ["대기열", "도움말"]
    }
    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    if content == u"대기열":
        data = db.get_data()
        now = datetime.datetime.now()
        text = "🐤️로스트아크 대기열 알림봇\n"
        text += "═══════════\n"
        text += f"{now.hour}시 {now.minute}분 {now.second}초 기준\n\n"

        for item in data:
            queue = item[1]
            if item[1] == -1:
                queue = '지원예정'

            text += f"{item[0]} : {queue}\n"

        dataSend = {
            "message": {
                "text": text
            }
        }
    elif content == u"도움말":
        dataSend = {
            "message": {
                "text": "1. 대기열\n\n 개발자 블로그 : http://suitee.me"
            }
        }
    else:
        dataSend = {
            "message": {
                "text": "명령어를 다시 입력해주세요. 1. 대기열, 2.도움말"
            }
        }

    dataSend["keyboard"] = {"type": "buttons", "buttons": ["대기열", "도움말"]}
    return jsonify(dataSend)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)