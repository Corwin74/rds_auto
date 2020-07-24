import logging
import requests
from bs4 import BeautifulSoup

MAX_PAGE = 36
MODEL = '3er'

logging.basicConfig(filename=MODEL+'.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.warning('is when this event was logged.')
with open(MODEL+'_links.txt', 'w', encoding='utf-8') as f:
    for i in range(1, MAX_PAGE + 1):
        response = requests.get("https://auto.ru/moskva/cars/bmw/"+MODEL+"/all/?output_type=list&page=" + str(i))
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, 'lxml')
            pages = bs.find('div', class_='ListingCars-module__container ListingCars-module__list')
            list_car = pages.find_all('div', class_='ListingItem-module__container')
            for it in list_car:
                url = it.find('a', class_='ListingItemTitle-module__link')
                f.write(str(url['href'] + '\n'))
    f.close()
