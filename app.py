import streamlit as st
from db.db_connector import get_db_connection
import pandas as pd


# Title of the app
st.title("Customer Order Data Engineering")

# Get the database connection engine
engine = get_db_connection()

#read data from the csv file
customer_data = pd.read_csv("data/customers.csv")
order_data = pd.read_csv("data/order.csv")

st.write(customer_data.head(5))
st.write(order_data.head(5))