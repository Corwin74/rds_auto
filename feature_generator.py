"""
Обучем CatBoostClassifier на собранном train датасете, в котором есть признак MODEL (1er, 5er, X5 и т.д.)
чтобы потом сгенерировать этот признак для датасета, на котором необходимо сделать предсказание
Обученную модель сохраняем, для использования в основном модуле.
На тесте модель показала 100 процентную точность для распространненых моделей (3 и 5 серия),
и около 97 процентов для малочисленных моделей (например 6-я серия)
"""

import pandas as pd
from catboost import CatBoostClassifier

# CATBOOST
ITERATIONS = 2000
LR = 0.05


def preproc_data(df_in):
    dfd = df_in.copy(deep=True)
    dfd['name'] = dfd['name'].apply(lambda x: x.split(' ')[0])
    dfd.drop(['brand', 'vehicleConfiguration', 'description', 'equipment', 'color', 'mileage', 'pts', 'owners',
             'wheel', 'state', 'customs', 'owningTime', 'Unnamed: 0', 'name_full', 'price'], axis=1, inplace=True)
    dfd['engineDisplacement'] = dfd.engineDisplacement.apply(lambda x: x.split(' ')[0])
    dfd['drive'] = dfd.drive.apply(lambda x: x.lower())
    dfd['enginePower'] = dfd.enginePower.apply(lambda x: int(x.split(' ')[0]))
    return dfd


df = pd.read_csv(r'C:\Users\Alex\PycharmProjects\untitled\data\auto_data_x.csv')
X = preproc_data(df)
y = X.iloc[:, -1]
X = X.iloc[:, :-1]


model_list = y.value_counts().index.to_list()
cat_features = ['bodyType', 'fuelType', 'name', 'vehicleTransmission', 'engineDisplacement', 'drive']
cls = CatBoostClassifier(iterations=1000, learning_rate=0.1, depth=None, class_names=model_list)
cls.fit(X, y, cat_features=cat_features, verbose=False)

# Сохраняем модель для последующией генерации признака 'model' для  "предсказательного" датасета

cls.save_model('model_feature_generator')
