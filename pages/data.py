import streamlit as st
from data_import import data_read_write
import pandas as pd

def data_upload_page_display():
    st.header("MySQL Data Insertion")
    st.write('lets import the dataset by clicking the import data button. it will make your dataset uploaded to mysql database')
    
    customer_data = pd.read_csv("data/customers.csv")
    order_data = pd.read_csv("data/order.csv")
    
    col1, col2, col3, col4, col5 =st.columns(5)
    with col1:
        st.button('Import Data', on_click=data_read_write, use_container_width=True)
        
    with col2:
        readmore_button = st.button("Read more", use_container_width=True)
    if readmore_button:
        st.write("""This is delivergate data engineering project task.
                     So, data used here is given by delivergate. 
                     There two datasets Customers and Orders given as .csv format.
                     please refer the dataframes below read from the .csv""")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Customers.csv",customer_data, "** Note **")
        with col2:
            st.write("Orders.csv",order_data)
        
        st.write("""
                 When you upload the dataset by clicking the Import Data button above, 
                 column names of the each table will be change slightly to make attribute names organized.
                 please refer below to findout the coulumns we changed.""")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text("""
                    Customers.csv
                    -------------
                    name - customer_name
                    email - customer_email
                    """)
        with col2:
            st.text(
                """
                Orders.csv
                ----------
                id - order_id
                created_at - order_date
                """)