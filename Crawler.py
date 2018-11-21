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

import json
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

class Crawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
    #     # options.add_argument('window-size=1920x1080')
    #     # options.add_argument("disable-gpu")
    #     self.driver = webdriver.Chrome(executable_path=r"chromedriver_win32/chromedriver.exe", chrome_options=options)
        self.driver = webdriver.Chrome(executable_path=r"/usr/local/bin/chromedriver", chrome_options=options)

    def start(self):
        url = 'https://rubystarashe.github.io/lostark/'

        self.driver.get(url)
        sleep(1)
        html = self.driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        servers = {}
        items = []

        now = datetime.now()
        servers['server_time'] = '%s-%s-%s %s시 %s분 기준' % (now.year, now.month, now.day, now.hour, now.minute)

        server_count = len(soup.select('span.data.name'))

        for i in range(server_count):
            server = soup.select('span.data.name')[i].text
            queue = soup.select('span.data.queue')[i].text
            items.append({"server": server, "queue": queue})

        servers["items"] = items

        # server_name = ''

        # for tag in soup.select('div.box')[0].text:
        #     server_name += tag.text

        # server_name = server_name.replace(' ', '').split("\n")

        # server_name = [x for x in server_name
        #                if "(" not in x and "상세" not in x and
        #                "서버" not in x and "대기열" not in x and
        #                "\xa0" not in x and "" != x]

        # for i, item in enumerate(server_name):
        #     if i % 2 == 0:
        #         items.append({"server": item, "wait": server_name[i + 1]})
        #
        # servers["items"] = items

        # json_file = json.dumps(servers, indent=2, ensure_ascii=False)
        self.driver.quit()
        return servers
