import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL,nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase,axis='columns',inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load = st.text('loading data...')
data = load_data(10000)
data_load.text('Done! using the cache and Loading data done .....')

# st.subheader('Exploring the raw data')
# st.write(data)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('number of pick ups by hourly data')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)
st.map(data)

hour = st.slider('hour', 0, 23, 17)
data_filtered = data[data[DATE_COLUMN].dt.hour == hour]
st.map(data_filtered)
