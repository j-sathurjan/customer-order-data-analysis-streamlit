"""
Data Import Module for Streamlit Application

This module handles the import of customer and order data from CSV files into
a MySQL database using SQLAlchemy. The `data_read_write` function reads the data,
renames columns as required, and then inserts the data into the database tables
if a valid database connection is established.

Functions:
- data_read_write: Reads data from CSV files, renames columns, and imports the data
  into MySQL tables. Provides success or error messages based on operation outcome.
"""
from db.db_connector import get_db_connection # Database connection function
import pandas as pd # Data manipulation library
import streamlit as st # Streamlit library for displaying messages

# Establish a database connection using SQLAlchemy engine
engine = get_db_connection()

def data_read_write():
    """
    Read Data from CSV and Write to MySQL Database.

    This function performs the following:
    - Reads data from `customers.csv` and `orders.csv` files located in the `data/` directory.
    - Renames columns to match MySQL database schema for consistent attribute naming.
    - Imports the modified dataframes into MySQL tables (`customers` and `orders`).
    - Provides success or error messages depending on the operation outcome.

    Exceptions:
    - Returns an error message if data import fails due to database connection issues or other errors.
    """
    try:
        # Load data from CSV files into pandas DataFrames
        customer_data = pd.read_csv("data/customers.csv")
        order_data = pd.read_csv("data/order.csv")
        
        # Rename columns for consistency with the MySQL database schema
        customer_data.rename(columns={'name':'customer_name','email':'customer_email'}, inplace=True)
        order_data.rename(columns={'id': 'order_id', 'created_at': 'order_date'}, inplace=True)

        # import dataframe into mqsql database if connection exist success else error
        if engine:
            # Import data to MySQL using SQLAlchemy's to_sql method
            customer_data.to_sql(name='customers', con=engine, if_exists='replace', index=customer_data.customer_id)
            order_data.to_sql(name='orders', con=engine, if_exists='replace', index=order_data.order_id)
            
            # Display a success message in Streamlit
            return st.success("Data imported successfully.")
        
        # Display an error message if the database connection is not established
        return st.error('Database connection error!.')
    
    except Exception:
        # Display a general error message if data import fails for any other reason
        return st.error(f"Something went wrong on data import!")
