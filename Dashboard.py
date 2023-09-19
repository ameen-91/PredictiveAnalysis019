import streamlit as st
import numpy as np
import pandas as pd
import time
import joblib as jb
from sklearn.pipeline import Pipeline

st.set_page_config(
    page_title="Condition Monitoring",
    page_icon='H'
)



data = pd.read_csv('data_aug.csv')


anomaly = jb.load('anomaly.pkl')


def predict_anomaly(i):
    pred = anomaly.predict(pd.DataFrame(data.iloc[i,:]).T)
    if pred<0:
        x = 'Abnormal'
    else:
        x = 'Normal'
    return x




st.title("Condition Monitoring")
update_interval = 1
update_interval = st.slider(min_value=1,max_value=5,value=None,label='Speed')

placeholder = st.empty()



for i in range(0,len(data)):

    with placeholder.container():

        element1,element2,element3 = st.columns(3)
        e4, e5, e6 = st.columns(3)
        e7, e8 = st.columns(2)
        e9, e10 = st.columns(2)

        element1.metric(value=data.loc[i,'Pressure (psi)'],label='Pressure (psi)')
        element2.metric(value=data.loc[i,'Temperature (°C)'],label='Temperature (°C)')
        element3.metric(value=data.loc[i,'Oil Flow (L/min)'],label='Oil Flow (L/min)')
        e4.metric(value=data.loc[i,'Vibration (mm/s)'],label='Vibration (mm/s)')
        e5.metric(value=data.loc[i,'Power Status'],label='Power Status')
        e6.metric(value=data.loc[i,'Oil Level (%)'],label='Oil Level (%)')
        e7.metric(value=data.loc[i,'Tool RPM (rpm)'],label='Tool RPM (rpm)')
        e8.metric(value=data.loc[i,'Current (A)'],label='Current (A)')
        e9.metric(value=data.loc[i,'Machine Status'],label='Machine Status')
        e10.metric(value=predict_anomaly(i),label='Anomaly')
        time.sleep(1/update_interval)

