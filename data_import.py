from db.db_connector import get_db_connection
import pandas as pd
import streamlit as st

# Get the database connection engine
engine = get_db_connection()

def data_read_write():
    try:
        #read data from the csv file
        customer_data = pd.read_csv("data/customers.csv")
        order_data = pd.read_csv("data/order.csv")
        customer_data.rename(columns={'name':'customer_name','email':'customer_email'}, inplace=True)
        order_data.rename(columns={'id': 'order_id', 'created_at': 'order_date'}, inplace=True)

        # import dataframe into mqsql database if connection exist success else error
        if engine:
            customer_data.to_sql(name='customers', con=engine, if_exists='replace', index=customer_data.customer_id)
            order_data.to_sql(name='orders', con=engine, if_exists='replace', index=order_data.order_id)
            return st.success("Data imported successfully.")
        return st.error('Database connection error!.')
    except Exception as e:
            return st.error(f"Something went wrong on data import! {e}")