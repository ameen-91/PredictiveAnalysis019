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



data = pd.read_csv('demonstrate_data.csv')

health = jb.load('predict.pkl')
prep = jb.load('prep.pkl')
anomaly = jb.load('anomaly.pkl')

features = ['Pressure (psi)',	'Temperature (°C)',	'Oil Flow (L/min)',	'Vibration (mm/s)','Oil Level (%)'	,'Tool RPM (rpm)' ,'Current (A)']
health_ft = ['Temperature (°C)','Tool RPM (rpm)']
pressure_cond = 'Normal'
temp_cond = 'Normal'
oil_cond = 'Normal'
rpm_cond = 'Normal'


def checks(i):

    pressure_psi = data.loc[i,'Pressure (psi)']
    temperature_c = data.loc[i,'Temperature (°C)']
    vibration_mm_s = data.loc[i,'Vibration (mm/s)']
    oil_level_percent = data.loc[i,'Oil Level (%)']
    tool_rpm_rpm = data.loc[i,'Tool RPM (rpm)']

    global pressure_cond, temp_cond, oil_cond, rpm_cond,vib_cond
    



    if pressure_psi > data['Pressure (psi)'].quantile(0.98):
        pressure_cond = 'Warning! Too High'
    elif pressure_psi < data['Pressure (psi)'].quantile(0.02):
        pressure_cond = 'Warning! Too Low'
    else:
        pressure_cond = 'Normal'

    if temperature_c > data['Temperature (°C)'].quantile(0.98):
        temp_cond = 'Warning! Too High'
    else:
        temp_cond = 'Normal'

    if oil_level_percent < data['Oil Level (%)'].quantile(0.02):
        oil_cond = 'Warning! Too Low'
    else:
        oil_cond = 'Normal'

    if tool_rpm_rpm > data['Tool RPM (rpm)'].quantile(0.98):
        rpm_cond = 'Warning! Too High'
    elif tool_rpm_rpm < data['Tool RPM (rpm)'].quantile(0.02):
        rpm_cond = 'Warning! Too Low'
    else:
        rpm_cond = 'Normal'
    
    if vibration_mm_s > data['Vibration (mm/s)'].quantile(0.98):
        vib_cond = 'Warning! Too High'
    elif vibration_mm_s < data['Vibration (mm/s)'].quantile(0.02):
        vib_cond = 'Warning! Too Low'
    else:
        vib_cond = 'Normal'

    return pressure_cond,temp_cond,oil_cond,rpm_cond

def predict_health(i):
    k = pd.DataFrame(data.loc[i,health_ft]).T
    feature_map = {'Temperature (°C)':'Process temperature','Tool RPM (rpm)':'Rotational speed'}
    features = ['Process temperature','Rotational speed']
    k = k.rename(columns=feature_map)
    k = prep.fit_transform(k)
    pred = health.predict(k)
    if pred != 0:
        x = 'Likely'
    else:
        x = 'Unlikely'
    return x
    
    


def predict_anomaly(i):
    pred = anomaly.predict(pd.DataFrame(data.loc[i,features]).T)
    if pred==-1:
        x = 'Abnormal'
    else:
        x = 'Normal'
    return x




st.title("Condition Monitoring")
update_interval = 1
update_interval = st.slider(min_value=1,max_value=5,value=None,label='Speed')

placeholder = st.empty()

status = 'sdf'

for i in range(0,len(data)):
    checks(i)
    with placeholder.container():      
        element1,element2,element3 = st.columns(3)
        e4, e5, e6 = st.columns(3)
        e7, e8 = st.columns(2)
        e9, e10 = st.columns(2)
        d1,d2= st.columns(2)
        d3,d4= st.columns(2)
        d5= st.empty()
        machine_health = st.empty()
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
        d1.write(f"Pressure Levels: {pressure_cond}")
        d2.write(f"Temperature Levels: {temp_cond}")
        d3.write(f"Oil Levels: {oil_cond}")
        d4.write(f"RPM Levels: {rpm_cond}")
        d5.write(f"Vibration Levels: {vib_cond}")
        machine_health.metric(value=predict_health(i),label='Temperature/RPM Failure')

        
        time.sleep(1/update_interval)

