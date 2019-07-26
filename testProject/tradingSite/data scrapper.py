import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testProject.settings')


import quandl
import pandas as pd
import numpy as np
from tradingSite.models import Commodity




uploaded_codes = {'Wheat': 'CHRIS/CME_W1', "Corn": 'CHRIS/CME_C1', 'Oats':'CHRIS/CME_O1','Rice':'CHRIS/CME_RR1', 'SoyBean':'CHRIS/CME_S1'}
codes = {'Coffee': 'CHRIS/ICE_KC1', 'COCOA BEANS':'CHRIS/ICE_CC1', 'Sugar': 'CHRIS/ICE_SB1'}


def clean_data(data):
    cleaned_data = pd.DataFrame(columns=['date', 'current_price', 'previous_price', 'change'])

    cleaned_data['date']=data.index
    if 'Settle' in data.columns:
        current_price = data['Settle'].astype(float)
        current_price.reset_index(drop=True,inplace=True)
        current_price = current_price.fillna(0)
        cleaned_data['current_price'] = current_price

    if 'Last' in data.columns:
        previous_price = data['Last'].astype(float)
        previous_price.reset_index(drop=True, inplace=True)
        previous_price = previous_price.fillna(0)
        cleaned_data['previous_price'] = previous_price

    elif 'High' in data.columns:
      previous_price = data['High']
      previous_price = previous_price.fillna(0)
      previous_price.reset_index(drop=True,inplace=True)
      previous_price = previous_price.astype(float)
      cleaned_data['previous_price'] = previous_price

    if 'Change' in data.columns:
        change = data['Change'].astype(float)
        change.reset_index(drop=True, inplace=True)
        change = change.fillna(0)
        cleaned_data['change'] = change


    return cleaned_data



def bulk_downlaod(coms,start_date ='2017-12-31', end_date = '2018-12-31'):
    '''grab data for a commodity from start_date to end_date'''


    for key in coms.keys():
        data = quandl.get(coms[key], start_date =start_date, end_date= end_date, collapse='daily')
        data = clean_data(data)
        name = [key]* data.shape[0]
        data['name'] = name
        com_instances = []
        for index, row in data.iterrows():
            com = Commodity(name=row['name'], current_price =row['current_price'], previous_price=row['previous_price'],
                                        change=row['change'],Date=row['date'])
            com_instances.append(com)

        Commodity.objects.bulk_create(com_instances)
        print(key, ': Uploaded')


#bulk_downlaod(codes)



