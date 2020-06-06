import telebot
import config
import requests
import time
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.TOKEN)

URL = 'https://www.avito.ru/kazan/avtomobili?cd=1&radius=200&s=104'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', 'accept': '*/*'}
HOST = 'https://avito.ru'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='snippet-horizontal')
    cars = []
    for el in items:
        cars.append({
            'Марка': el.find('a', class_='snippet-link').get_text(strip=True),
            'Цена': el.find('span', class_='snippet-price').get_text(strip=True),
            'Данные': el.find('div', class_='specific-params').get_text(strip=True),
            'Ссыкла': HOST + el.find('a', class_='snippet-link').get('href')
         })
    for el in cars:
        # print(str(el.values()))
        # 'запись в ссылок в txt'
        txtLinks = open('LinksCar.txt', 'r')
        text = txtLinks.read()
        txtLinks.close()
        print(text.count(str(el.get('Ссыкла'))))
        if text.count(str(el.get('Ссыкла'))) == 0:
            Links = open('LinksCar.txt', 'a')
            Links.write(str(el.get('Ссыкла')) + '\n')
            bot.send_message(854949272, str(el.values()).replace('dict_values', ''))
            # bot.send_message(466788624, str(el.values()).replace('dict_values', ''))
            # bot.send_message(155855643, str(el.values()).replace('dict_values', ''))
            # bot.send_message(474196689, str(el.values()).replace('dict_values', ''))
            txtLinks.close()
        else:
            print('Пук')


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('PuK')


# carTxt = open('LinksCar.txt')
# for lineTxt in carTxt:
#     print('link - ' + lineTxt)
while True:
    parse()
    time.sleep(20)


