# Выбираем авто выгодно
Соревнование по предсказанию цены на автомобили по его характеристикам.

Необходимо предсказать цену на автомобиль по его характеристикам. Особенностью соревнования является отсутствие данных. Их необходимо спарсить с сайтов по продаже автомобилей.

Сбор данных:

auto_ru_to_links.py - Служит для формирования файла с ссылками на конкретную модель  
links_to_csv.py - Из файла сформированного выше считывает ссылки, парсит информацию по этим ссылкам
и формирует файл в формате csv c полученными данными.  
MergeData.ipynb - Объединяет файлы с данными по сериям машин в единый train датасет  
feature_generator.py - Обучение модели на собранных данных и ее сохранение, для добавления признака 'model' в датсет, на котором делаем предсказание для submission  
Stack.ipynb - Итоговый ноутбук  
