import pandas as pd
import numpy as np
import sys
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from tqdm.notebook import tqdm
from catboost import CatBoostRegressor, CatBoostClassifier
import re
from sklearn.metrics import classification_report



VAL_SIZE   = 0.25   # 25%
N_FOLDS    = 5
RANDOM_SEED = 42

# CATBOOST
ITERATIONS = 2000
LR         = 0.05


def preproc_test(df):
    df = df.drop('brand', axis=1)
    df['name'] = df['name'].apply(lambda x: x.split(' ')[0])
    df.drop(['vehicleConfiguration', 'description', 'Комплектация',
              'Руль','Состояние', 'Таможня', 'Владение', 'id', 
             'color', 'mileage', 'ПТС', 'Владельцы'], axis=1, inplace=True)
    df['engineDisplacement'] = df.engineDisplacement.apply(lambda x: x.split(' ')[0])
    df['modelDate'] = df.modelDate.apply(lambda x: int(x))
    df['numberOfDoors'] = df.numberOfDoors .apply(lambda x: int(x))
    df['Привод'] = df['Привод'].apply(lambda x: x.lower())
    df['enginePower'] = df.enginePower.apply(lambda x: int(x.split(' ')[0]))
    df['productionDate'] = df['productionDate'].apply(lambda x: int(x))
    return df



def preproc_data(df):

    df['name'] = df['name'].apply(lambda x: x.split(' ')[0])
    df.drop(['brand', 'vehicleConfiguration', 'description', 'equipment', 'color', 'mileage', 'pts', 'owners',
              'wheel','state', 'customs', 'owningTime', 'Unnamed: 0', 'name_full', 'price'], axis=1, inplace=True)
    df['engineDisplacement'] = df.engineDisplacement.apply(lambda x: x.split(' ')[0])
    df['drive'] = df.drive.apply(lambda x: x.lower())
    df['enginePower'] = df.enginePower.apply(lambda x: int(x.split(' ')[0]))
    return df


df = pd.read_csv(r'C:\Users\Alex\PycharmProjects\untitled\data\auto_data_x.csv')
dft = pd.read_csv('test.csv')
X_for_pred = preproc_test(dft)
X = preproc_data(df)
y = X.iloc[:,-1]
X = X.iloc[:,:-1]
X_for_pred.columns = X.columns

model_list = y.value_counts().index.to_list()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=VAL_SIZE, shuffle=True, 
    random_state=RANDOM_SEED, stratify=y)

cat_features = ['bodyType', 'fuelType', 'name', 'vehicleTransmission', 'engineDisplacement', 'drive']
cls = CatBoostClassifier(iterations=1000, learning_rate=0.1, depth=None, class_names = model_list)

cls.fit(X, y, cat_features=cat_features, verbose=False)

#Сохраняем модель для последующией генерации признака 'model' для  "предсказательного" датасета

cls.save_model('model_feature_generator')

