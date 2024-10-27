"""
Streamlit Application: Customer Order Data Engineering Dashboard

This application is built with Streamlit and provides an interactive dashboard
for data analysis and machine learning on customer order data.
The app includes three main pages:
1. Dashboard: Provides data visualizations, filters, and key metrics.
2. Original Data: Allows users to upload CSV files to a MySQL database and give insights about data.
3. Machine Learning: Displays machine learning predictions and insights.

Each page is implemented as a function, keeping the code modular and organized.

Modules:
- data(): Displays the contents of "Original Data" page by calling data_upload_page_display.
- home(): Displays the Dashboard page, calling functions for filtering, visualizations, and metrics.
- ml(): Displays the Machine Learning page with ML model predictions or processing insights.

Author: Sathurjan Jeyarupan
"""
# Import necessary libraries
import streamlit as st # Streamlit library for web application interface
from db.db_connector import get_db_connection # Function to establish database connection
import pandas as pd # Data manipulation and analysis library

# Import page-specific functions for a modular code structure
from pages.dashboard import data_filtering, dashboard_data_visualization,dashboard_key_metrics_display
from pages.data import data_upload_page_display
from pages.ml import ml_data_processing_display

# Basic configuration for the Streamlit app
st.set_page_config(
    # Title of the app
    page_title="Customer Order Data Engineering", # Sets the title displayed in the browser tab
    page_icon="🦜",) # Sets the icon for the app

# Establish a database connection using SQLAlchemy engine
engine = get_db_connection()

def data():
    """
    Display the Original Data Page for data import.
    
    This function manages the page for uploading and processing data from CSV files.
    It calls `data_upload_page_display` from the data page module to handle the user interface 
    and processing related to data uploads.
    """
    data_upload_page_display() # Display data upload interface and processing

def home():
    """
    Display the Dashboard Page.
    
    This function manages the main dashboard page, including:
    - Data filtering options based on user input.
    - Data visualizations like bar and line charts.
    - Display of key metrics, such as total revenue, nomber of orders and number of unique customers.
    
    It sequentially calls `data_filtering`, `dashboard_data_visualization`, 
    and `dashboard_key_metrics_display` functions to display the page content.
    """
    data_filtering() # Applies filters for data based on user input and displays the filtered data
    dashboard_data_visualization() # Displays data visualizations on the dashboard
    dashboard_key_metrics_display() # Displays summary metrics for quick insights
    
def ml():
    """
    Display the Machine Learning Page.
    
    This function manages the machine learning page, where users can view or 
    generate predictions using customer order data.
    It calls `ml_data_processing_display` from the ML page module to show ML 
    model results and insights.
    """
    ml_data_processing_display() # Show machine learning results and processing interface
    
# Define the three main pages of the application
home_page = st.Page(home, title="Dashboard") # Main dashboard page for visualizations and insights
data_page = st.Page(data, title="Original Data") # Original Data page for importing CSVs to MySQL and insights
ml_page = st.Page(ml, title="Machine Learning") # Machine learning page for customer behavior predictions

# Set up navigation for the app with Streamlit's page navigation system and display the selected page
pg = st.navigation([home_page, data_page, ml_page])
pg.run() # Run the selected page