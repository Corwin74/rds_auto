"""
Модуль читает по одной ссылки из заранее сформированного файла с ссылками на страницу
с предложением конкретной машины, парсит ее и записывает инфомацию в файл формата csv
Режим полуавтоматичский, необходимо указать серию в константе MODEL.
На выходе получаем файл с именем типа: MODEL_data.csv, например x7_data.csv
"""

import csv
import requests
from bs4 import BeautifulSoup
import logging
import re
from tqdm import tqdm

MODEL = 'x7'  # Указываем серию BMW, которую будем парсить
FIELDS_LIST = ['bodyType', 'brand', 'color', 'fuelType', 'modelDate', 'name', 'name_full', 'numberOfDoors',
               'productionDate', 'vehicleConfiguration',
               'vehicleTransmission', 'engineDisplacement', 'enginePower', 'description', 'mileage', 'equipment',
               'drive', 'wheel',
               'state', 'owners', 'pts', 'customs', 'owningTime', 'price']

logging.basicConfig(filename=MODEL + '.log', filemode='w', level=logging.WARNING, format='%(asctime)s %(message)s')
logging.warning('is when this event was logged.')


def get_record(url_link):
    """
    Функция получает ссылку на предложение о продаже, парсит страницу
    Если парсинг удачный возвращает список с полученными значениями.
    Если цена не найдена или возникла ошибка обработки возвращает строку 'sale'
    """
    url_link = re.sub(r"^\s+|\n|\r|\s+$", '', url_link)
    resp = requests.get(url_link)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        bs = BeautifulSoup(resp.text, 'lxml')
        try:
            equip_dict = {}
            equipment_title = bs.find('div', class_='CardComplectation__groups')
            if equipment_title:
                equip_group = equipment_title.find_all('div', class_='CardComplectation__group')
                for it in equip_group:
                    eq_group = it.find('span', class_="CardComplectation__itemName").text
                    equip_dict[eq_group] = []
                    for item in it.find_all('li', class_="CardComplectation__itemContentEl"):
                        equip_dict[eq_group].append(item.text)

            card = bs.find('div', class_=re.compile(r'CardOfferBody__.{20}'))
            card_info = card.find('ul', class_='CardInfo')
            sidebar_meta = bs.find('div', class_="LayoutSidebar")

            # fields
            temp_check = sidebar_meta.find('meta', itemprop="price")
            if temp_check.has_attr('content'):
                price = temp_check['content']
            else:
                logging.warning('Has been sold ' + url_link)
                return 'sale'
            bodyType = sidebar_meta.find('meta', itemprop="bodyType")['content']
            brand = 'bmw'
            color = sidebar_meta.find('meta', itemprop="color")['content']
            fuelType = sidebar_meta.find('meta', itemprop="fuelType")['content']
            modelDate = sidebar_meta.find('meta', itemprop="modelDate")['content']
            numberOfDoors = sidebar_meta.find('meta', itemprop="numberOfDoors")['content']
            productionDate = sidebar_meta.find('meta', itemprop="productionDate")['content']
            vehicleConfiguration = sidebar_meta.find('meta', itemprop="vehicleConfiguration")['content']
            vehicleTransmission = sidebar_meta.find('meta', itemprop="vehicleTransmission")['content']
            engineDisplacement = sidebar_meta.find('meta', itemprop="engineDisplacement")['content']
            enginePower = sidebar_meta.find('meta', itemprop="enginePower")['content']
            description = re.sub(r"^\s+|\n|\r|\s+$", '', sidebar_meta.find('meta', itemprop="description")['content'])
            equipment = str(equip_dict)
            if card_info:  # машина с пробегом
                name_full = sidebar_meta.find_all('meta', itemprop="name")[0]['content']
                name = sidebar_meta.find_all('meta', itemprop="name")[7]['content']
                find_res = card_info.find('li', class_="CardInfo__row CardInfo__row_kmAge")
                drive = card_info.find('li', class_="CardInfo__row_drive"). \
                    find_all('span', class_='CardInfo__cell')[1].text.lower()
                wheel = card_info.find('li', class_="CardInfo__row_wheel"). \
                    find_all('span', class_='CardInfo__cell')[1].text
                state = card_info.find('li', class_="CardInfo__row_state"). \
                    find_all('span', class_='CardInfo__cell')[1].text
                owners = card_info.find('li', class_="CardInfo__row_ownersCount"). \
                    find_all('span', class_='CardInfo__cell')[1].text
                pts = card_info.find('li', class_="CardInfo__row_pts").find_all('span', class_='CardInfo__cell')[1].text
                customs = card_info.find('li', class_="CardInfo__row_customs"). \
                    find_all('span', class_='CardInfo__cell')[1].text
                temp_ot = card_info.find('li', class_="CardInfo__row_owningTime")
                if find_res:
                    mileage = find_res.find_all('span', class_='CardInfo__cell')[1].text
                else:
                    mileage = 0
                if temp_ot:
                    owningTime = temp_ot.find_all('span', class_='CardInfo__cell')[1].text
                else:
                    owningTime = ''
            else:  # машина новая
                price = re.findall(r'\d+', card.find('span', class_='OfferPriceCaption__price').text)
                price = ''.join(price)
                card_new_trans = card.find('li', class_='CardInfoGrouped__row CardInfoGrouped__row_drive')
                drive = card_new_trans.find('div', class_='CardInfoGrouped__cellValue').text.lower()
                wheel = 'Левый'
                state = 'Не требует ремонта'
                owners = 0
                pts = 'Оригинал'
                customs = 'Растаможен'
                owningTime = '0'
                mileage = '0'
                name = sidebar_meta.find_all('meta', itemprop="name")[6]['content']
                name_full = sidebar_meta.find_all('meta', itemprop="name")[0]['content']

            return [bodyType, brand, color, fuelType, modelDate, name, name_full, numberOfDoors, productionDate,
                    vehicleConfiguration,
                    vehicleTransmission, engineDisplacement, enginePower, description, mileage, equipment, drive, wheel,
                    state, owners, pts, customs, owningTime, price]

        except (AttributeError, IndexError, KeyError) as e:
            logging.error(e, exc_info=True)  # Пишем возникшую ошибку
            logging.error(url_link)  # и ссылку в которой она возникла
            return 'sale'

    else:
        logging.warning(url_link + str(resp.status_code))
        return 'sale'


with open(r'C:\Users\Alex\PycharmProjects\untitled\\' + MODEL + '_links.txt') as f:
    with open(MODEL + '_data.csv', 'w', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(FIELDS_LIST)
        for line in tqdm(f.readlines()):
            temp = get_record(re.sub(r"^\s+|\n|\r|\s+$", '', line))
            if temp != 'sale':
                csv_writer.writerow(temp)
