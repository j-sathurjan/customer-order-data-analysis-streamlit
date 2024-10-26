import streamlit as st
from db.db_connector import get_db_connection
import pandas as pd
from pages.dashboard import data_filtering, dashboard_data_visualization,dashboard_key_metrics_display
from pages.data import data_upload_page_display
from pages.ml import ml_data_processing_display

# Get the database connection engine
engine = get_db_connection()

#Page configuration
st.set_page_config(
    # Title of the app
    page_title="Customer Order Data Engineering",
    page_icon="🧊",)

def data():
    data_upload_page_display()

def home():
    data_filtering()
    dashboard_data_visualization()
    dashboard_key_metrics_display()
    
def ml():
    ml_data_processing_display()
    
home_page = st.Page(home, title="Dashboard")
data_page = st.Page(data, title="Original Data")
ml_page = st.Page(ml, title="Machine Learning")

pg = st.navigation([home_page, data_page, ml_page])
pg.run()