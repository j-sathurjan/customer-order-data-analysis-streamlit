"""
Data Upload Page Module for Streamlit Application

This module manages the "Data Page" in the Streamlit app, allowing users to import customers 
and orders data from CSV files into a MySQL database. The page displays brief information about the data 
and guides users on how to upload it. The `data_read_write` function handles data insertion to the database.

Functions:
- data_upload_page_display: Displays the UI for data upload and handles button actions for data import.
"""
#import necessory libraries
import streamlit as st # Streamlit library for app interface
from db.data_import import data_read_write # Function for reading and writing data to MySQL
import pandas as pd # Library for data manipulation

def data_upload_page_display():
    """
    Display the Data Upload Page.

    This function renders the UI for the data upload page, including:
    - A header and brief instructions for data upload.
    - Two main buttons: "Import Data" for uploading CSV data to MySQL and "Read More" for additional info.
    - Sample data tables displaying data from customers.csv and order.csv.
    - Column name mapping information for how data is standardized in the database.
    """
    try:
        # Page header and initial instructions
        st.header("MySQL Data Insertion")
        st.write("lets import the dataset by clicking the Import Data button."
                 "it will make your dataset uploaded to mysql database.")
        
        # Load the data from CSV files for display
        customer_data = pd.read_csv("data/customers.csv")
        order_data = pd.read_csv("data/order.csv")
        
        # Layout for buttons and interactive actions
        col1, col2, col3, col4, col5 =st.columns(5) # Columns for button layout
        with col1:
            # Button to import data to MySQL, triggers `data_read_write`
            st.button('Import Data', on_click=data_read_write, use_container_width=True)
            
        with col2:
            # "Read More" button to provide additional information
            readmore_button = st.button("Read more", use_container_width=True)
        
        # Display additional information when "Read More" is clicked
        if readmore_button:
            st.write("""
                This is part of the Delivergate Data Engineering project.
                The data provided here includes two datasets: Customers and Orders, both in .csv format.
                Below are previews of each dataset:
            """)
            
            # Display sample data from both CSVs
            col1, col2 = st.columns(2)
            with col1:
                st.write("Customers.csv",customer_data, "** Note **")
            with col2:
                st.write("Orders.csv",order_data)
            
            # Explain changes in column names to align with database schema
            st.write("""
                When you upload the dataset by clicking the Import Data button, 
                some column names in each table will be slightly modified to improve organization.
                Refer to the table below for the updated column names.
            """)
            
            # Display column name mappings for clarity
            col1, col2 = st.columns(2)
            with col1:
                st.text("""
                    Customers.csv
                    -------------
                    name -> customer_name
                    email -> customer_email
                """)
            with col2:
                st.text("""
                    Orders.csv
                    ----------
                    id -> order_id
                    created_at -> order_date
                """)
    except Exception:
        # Display error message if CSV file paths are incorrect
        return st.error("data path not correct!")
