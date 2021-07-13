""" Модуль для сбора ссылок с auto.ru на конкретную модель BMW.
    Работает в полуавтоматичском режиме.
    В константе MODEL указываем модель для которой будут собираться ссылки.
    На странице по адресу типа: https://auto.ru/moskva/cars/bmw/1er/all/
    внизу смотрим общее количество страниц для данной модели и указываем
    в константе MAX_PAGE
    Далее модуль перебирает всe страницы с предложениями, находит на каждой ссылки
    и записывает их в файл для дальнейшего парсинга.
"""

import logging
import requests
import os
from bs4 import BeautifulSoup

MAX_PAGE = 3
MODEL = 'i3'

logging.basicConfig(filename=MODEL + '.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.warning('is when this event was logged.')
print('Processing ' + MODEL)
cwd = os.getcwd()
with open(cwd + r'/data/' + MODEL + '_links_new.txt', 'w', encoding='utf-8') as f:
    for i in range(1, MAX_PAGE + 1):
        response = requests.get("https://auto.ru/cars/bmw/" + MODEL + "/all/?output_type=table&page=" + str(i))
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, 'lxml')
            #pages = bs.find('div', class_='ListingCars-module__container ListingCars-module__list')
            list_car = bs.find_all('div', 'ListingItemSequential-module__container')   # находим все теги с ссылками
            for it in list_car:
                url = it.find('a', class_='ListingItemTitle__link')   # находим ссылку
                f.write(str(url['href'] + '\n'))
    f.close()
