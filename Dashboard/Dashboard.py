import streamlit as st
import numpy as np
import pandas as pd
import time
import joblib as jb
from sklearn.pipeline import Pipeline
import plotly.express as px

st.set_page_config(
    page_title="Condition Monitoring",
    page_icon='H'
)



data = pd.read_csv('demonstrate_data.csv')

health = jb.load('PredictiveAnalysis019/predict.pkl')
prep = jb.load('PredictiveAnalysis019/prep.pkl')
anomaly = jb.load('PredictiveAnalysis019/anomaly.pkl')

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




st.title("Dashboard")
update_interval = 1
update_interval = st.slider(min_value=1,max_value=5,value=None,label='Speed')

placeholder = st.empty()

#status = 'sdf'

#run = pd.DataFrame(columns=data.columns)

for i in range(1,len(data)):
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
        ##fig_col1, fig_col2 = st.columns(2)
        element1.metric(value=data.loc[i,'Pressure (psi)'],label='Pressure (psi)',delta=round((data.loc[i,'Pressure (psi)']-data.loc[i-1,'Pressure (psi)'])))
        element2.metric(value=data.loc[i,'Temperature (°C)'],label='Temperature (°C)',delta=round((data.loc[i,'Temperature (°C)']-data.loc[i-1,'Temperature (°C)'])))
        element3.metric(value=data.loc[i,'Oil Flow (L/min)'],label='Oil Flow (L/min)',delta=round((data.loc[i,'Oil Flow (L/min)']-data.loc[i-1,'Oil Flow (L/min)'])))
        e4.metric(value=data.loc[i,'Vibration (mm/s)'],label='Vibration (mm/s)',delta=round((data.loc[i,'Vibration (mm/s)']-data.loc[i-1,'Vibration (mm/s)'])))
        e5.metric(value=data.loc[i,'Power Status'],label='Power Status')
        e6.metric(value=data.loc[i,'Oil Level (%)'],label='Oil Level (%)',delta=round((data.loc[i,'Oil Level (%)']-data.loc[i-1,'Oil Level (%)'])))
        e7.metric(value=data.loc[i,'Tool RPM (rpm)'],label='Tool RPM (rpm)',delta=round((data.loc[i,'Tool RPM (rpm)']-data.loc[i-1,'Tool RPM (rpm)'])))
        e8.metric(value=data.loc[i,'Current (A)'],label='Current (A)',delta=round((data.loc[i,'Current (A)']-data.loc[i-1,'Current (A)'])))
        e9.metric(value=data.loc[i,'Machine Status'],label='Machine Status')
        e10.metric(value=predict_anomaly(i),label='Anomaly')
        d1.write(f"Pressure Levels: {pressure_cond}")
        d2.write(f"Temperature Levels: {temp_cond}")
        d3.write(f"Oil Levels: {oil_cond}")
        d4.write(f"RPM Levels: {rpm_cond}")
        d5.write(f"Vibration Levels: {vib_cond}")
        machine_health.metric(value=predict_health(i),label='Temperature/RPM Failure')
        new_row = pd.Series(data.loc[i,data.columns])
        #un = run.append(new_row, ignore_index=True)

        
        '''with fig_col1:
            st.markdown("### First Chart")
            fig = px.bar(data_frame=data, y = data'Pressure (psi)')
            st.write(fig)
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame = data, y = 'Temperature (°C)')'''

        
        time.sleep(1/update_interval)

