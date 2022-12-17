import pandas as pd
import urllib.parse
import numpy as np
import itertools
#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import plotly.offline as pyoff
import plotly.graph_objs as go
from sklearn import preprocessing
from prophet import Prophet
from sklearn.metrics import mean_absolute_percentage_error
import os

def proceso():
    df = pd.read_csv(get_api_call(
    ["455.1_VENTAS_PRETES_0_M_25_98"],
    format="csv", start_date=2017
    ))
    # Convert Date to datetime Prepara para correr Prophet
    df['indice_tiempo'] = pd.to_datetime(df['indice_tiempo'])
    df.columns = ['ds', 'y']
    # corremos prophet
    m=Prophet(weekly_seasonality=True)
    fitted= m.fit(df)
    future = m.make_future_dataframe(periods=1, freq='MS')
    fcst = m.predict(future)
    #grabo en un csv
    
    print("Path at terminal when executing this file")
    print(os.getcwd() + "\n")
    print("This file path, relative to os.getcwd()")
    print(__file__ + "\n")

    dirpath = os.getcwd()
    outputpath = os.path.join(dirpath,'./dags/historico.csv')
    Outp=fcst[['ds', 'yhat']].merge(df,on='ds',how='left')
    Outp.to_csv(outputpath)
   
    return


#df.to_csv(local_filepath, header=False, index=False, quoting=1)

def get_api_call(ids, **kwargs):
    API_BASE_URL = "https://apis.datos.gob.ar/series/api/"
    kwargs["ids"] = ",".join(ids)
    return "{}{}?{}".format(API_BASE_URL, "series", urllib.parse.urlencode(kwargs))

def _get_monthly_sales():
    df = pd.read_csv(get_api_call(
    ["455.1_VENTAS_PRETES_0_M_25_98"],
    format="csv", start_date=2017
    ))
    return df


def _calculate_monthly_sales_forecast():
    df= _get_monthly_sales()
    # Convert Date to datetime Prepara para correr Prophet
    df['indice_tiempo'] = pd.to_datetime(df['indice_tiempo'])
    df.columns = ['ds', 'y']
    # corremos prophet
    m=Prophet(weekly_seasonality=True)
    fitted= m.fit(df)
    future = m.make_future_dataframe(periods=1, freq='MS')
    fcst = m.predict(future)
    # el valor pronosticado para el proximo mes seria
    pron=fcst[-1]
    # calculamos mape
    pred1=fcst[:-1]
    pred=pred1['yhat']
    true=df['y']
    mape=mean_absolute_percentage_error(true,pred)
    #escribir en el csv date y yhat
    return pron, mape
