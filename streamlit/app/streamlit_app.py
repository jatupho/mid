import streamlit as st
import pandas as pd
from urllib.request import urlopen
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import json
import requests
from streamlit_lottie import st_lottie
import pydeck as pdk
import snowflake.connector
from sqlalchemy import create_engine
import subprocess


#Layout
st.set_page_config(
    page_title="Midterm",
    layout="wide",
    initial_sidebar_state="expanded")

#Data Pull and Functions
st.markdown("""
<style>
.big-font {
    font-size:80px !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)

@st.cache_data
def pull_clean():
    master_zip=pd.read_csv('MASTER_ZIP.csv',dtype={'ZCTA5': str})
    master_city=pd.read_csv('MASTER_CITY.csv',dtype={'ZCTA5': str})
    return master_zip, master_city
@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        lottie_data = json.load(f)
        return json.dumps(lottie_data)


#Options Menu
with st.sidebar:
    selected = option_menu('Midterm', ["Database", 'Average','Graph'], 
        icons=['bi bi-inboxes-fill','bi bi-lungs-fill','bi bi-kanban-fill'],menu_icon='bi bi-incognito', default_index=0)
    
    
    
        


    

# กำหนด DATABASE_URL
DATABASE_URL = "postgresql://payet:root@4.191.73.176:5432/postgres"

# ใช้ create_engine เพื่อเชื่อมต่อกับฐานข้อมูล PostgreSQL
engine = create_engine(DATABASE_URL)

# อ่านข้อมูลจากตาราง waterdata ด้วย pandas
query = "SELECT * FROM waterdata"
df = pd.read_sql(query, engine)
average_by_year = df.groupby('year').agg({
    'water_data_front': 'mean',
    'water_data_back': 'mean',
    'water_drain_rate': 'mean'
})
# แสดงข้อมูล
if selected=="Database":
        df
        button_clicked = st.button('คลิกเพื่อเพิ่มข้อมูล')
        if button_clicked:
                subprocess.run(['python', 'genMockdata.py'])
                st.write('คุณได้เพิ่มข้อมูล!')

                
if selected=="Average":
        

# แสดงข้อมูล
        st.write("ค่าเฉลี่ยในแต่ละปี:")
        col1, col2, col3 = st.columns(3)

        with col1:
                st.subheader("waterfront")
                st.write(average_by_year['water_data_front'])

        with col2:
                st.subheader("waterback")
                st.write(average_by_year['water_data_back'])

        with col3:
                st.subheader("waterrate")
                st.write(average_by_year['water_drain_rate'])
        st.divider()
if selected=='Graph':
        st.write("กราฟเส้น:")
        st.plotly_chart(px.line(average_by_year, title='Average Water Data'))
        st.divider()
        st.write("กราฟแท่ง:")
        st.plotly_chart(px.bar(average_by_year, title='Average Water Data'))
        st.divider()

        st.plotly_chart(px.line(average_by_year, title='WaterDataFront'))
        st.plotly_chart(px.line(average_by_year, title='WaterDataBack'))
        st.plotly_chart(px.line(average_by_year, title='WaterDrainRate'))
