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
from datetime import datetime
from crawler import *

app = Flask(__name__)

@app.route('/keyboard')
def Keyboard():
    data_send = {
        "type": "buttons",
        "buttons": ["대기열", "도움말"]
    }
    return jsonify(data_send)


@app.route('/message', methods=['POST'])
def Message():
    data_receive = request.get_json()
    content = data_receive['content']
    if content == u"대기열":
        db = DbTools(select_only=True)
        data = db.get_data()
        now = datetime.now()
        text = "🐤️로스트아크 대기열 알림봇\n"
        text += "═══════════\n"
        text += f"{now.hour}시 {now.minute}분 {now.second}초 기준\n\n"

        for item in data:
            queue = item[1]
            if item[1] == -1:
                queue = '지원예정'

            text += f"{item[0]} : {queue}\n"
        text += f"\n데이터 제공 :\nrubystarashe.github.io/lostark\n"
        db.close()

        data_send = {
            "message": {
                "text": text
            }
        }
    elif content == u"도움말":
        data_send = {
            "message": {
                "text": "도움말 목록\n\n═══════════\n1. 대기열\n\n2. 도움말"
            }
        }
    else:
        data_send = {
            "message": {
                "text": "명령어를 다시 입력해주세요.\n1. 대기열\n\n2. 도움말"
            }
        }

    data_send["message"].update({'message_button': {'label': '개발자 윤옴므 블로그', 'url': 'http://suitee.me'}})
    data_send["keyboard"] = {"type": "buttons", "buttons": ["대기열", "도움말"]}
    return jsonify(data_send)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)