import pywebio
from pywebio.input import *
from pywebio.output import *
import requests
import folium
import os
import tornado.ioloop
import sys

try:

    def stop_tornado():
        tornado.ioloop.IOLoop.instance().stop()

    def get_ans():
        ans = radio(
            "Выберите действие:",
            options=['На главную', 'Выйти'])

        if ans == None:
            put_text("Ошибка! Ответ не может быть пустым!")
            main()

        if ans == 'На главную':
            clear()
            main()

        if ans == 'Выйти':
            stop_tornado()
            sys.exit()

    def get_info(ip = '127.0.0.1'):
        try:
            response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
            data = {
                '[IP]' : response.get('query'),
                '[Провайдер]' : response.get('isp'),
                '[Организация]' : response.get('org'),
                '[Страна]' : response.get('country'),
                '[Регион]' : response.get('regionName'),
                '[Город]' : response.get('city'),
                '[Почтовый код]' : response.get('zip'),
                '[Широта]' : response.get('lat'),
                '[Долгота]' : response.get('lon'),
            }
            for k, v in data.items():
                put_text(f'{k} : {v}')
            put_text('\n')
            agree = radio(
                "Сохранить карту в формате html?",
                options=['Да', 'Нет'])

            if agree =="Да":
                area = folium.Map(location=[response.get('lat'), response.get('lon')], zoom_start=8, titles="Цель")
                mark = folium.Marker(location=[response.get('lat'), response.get('lon')], popup="Цель",
                                     icon=folium.Icon(color='red')).add_to(area)
                name = response.get("query") + '_' + response.get("city") + '.html'
                area.save(f'{response.get("query")}_{response.get("city")}.html')
                path = os.path.abspath(name)
                obr =os.path.normpath(path)
                os.startfile(obr)
                get_ans()
            else:
                get_ans()

        except requests.exceptions.ConnectionError:
            put_text('[!] Проблемы с соединением!')

    def main():
        clear()
        put_text('IP INFORMATOR')
        ip = input("Введите IP: ")
        ip = "".join(ip.split())
        get_info(ip=ip)

    if __name__ == '__main__':
        main()

except pywebio.exceptions.SessionClosedException:
    tornado.ioloop.IOLoop.instance().stop()
    os.system('taskkill /f /im IP_INFORMATOR.exe')