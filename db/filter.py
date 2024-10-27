"""
Filter Module for Streamlit Application

This module provides functions for filtering and retrieving data from the database
for the Streamlit application. It includes functions to:
1. Get maximum filter amounts for user-defined thresholds.
2. Filter orders and customers based on date range, total spent, and order count.
3. Retrieve top customers by revenue.
4. Get total revenue and order count over time.
5. Summarize total revenue, unique customers, and order counts.

Functions:
- get_max_filter_amount: Retrieves maximum spent amount and order count for filtering.
- filter_data_by_sidebar: Filters orders based on user-defined criteria.
- filter_customer_by_amount: Filters customers based on spending and order count.
- top_customer_by_revenue: Retrieves the top customers by total revenue.
- get_total_over_time: Fetches revenue data grouped by year and month.
- get_total_summery: Returns summary metrics for total revenue, customers, and orders.
"""

# import neccessory libraries
from db.db_connector import get_db_connection # Import database connection function
import pandas as pd # Data manipulation library
import streamlit as st # Streamlit for UI interaction
from datetime import date # Date handling

# Establish a database connection using SQLAlchemy engine
engine = get_db_connection()

def get_max_filter_amount():
    """
    Retrieve Maximum Filter Amounts.

    This function retrieves the maximum spent amount and order count 
    from the database for setting user-defined filters.

    Returns:
        tuple: Maximum amount and maximum order count.
    Raises:
        Exception: If there is an error during database interaction.
    """
    try:
        # Check if the database engine is available
        if engine:
            # Query for maximum spent amount and order count per customer
            query = """
                SELECT MAX(spent_amount) max_amount, MAX(order_count) max_count
                FROM (SELECT SUM(total_amount) spent_amount, COUNT(order_id) order_count
                    FROM orders
                    GROUP BY customer_id) sum_table;
            """
            # Execute the SQL query and store the result in a DataFrame
            max_df = pd.read_sql(query, con=engine)
            
            # Return the maximum spent amount and order count as integers
            return int(max_df['max_amount']), int(max_df['max_count'])
        return st.error("Database connection error!") # Handle database connection error
    
    except Exception:
        return st.error("something went wrong on filtering!") # Handle general errors

def filter_data_by_sidebar(date_range, min_amount=0, min_orders=0):
    """
    Filter Orders Based on User-defined Criteria.

    This function filters the orders based on the date range, minimum amount spent, 
    and minimum number of orders by customers.

    Parameters:
        date_range (tuple): A tuple containing the start and end dates for filtering.
        min_amount (float): The minimum amount spent by customers for filtering (default is 0).
        min_orders (int): The minimum number of orders placed by customers for filtering (default is 0).

    Returns:
        DataFrame: A DataFrame containing filtered orders.
    Raises:
        Exception: If there is an error during database interaction.
    """
    try:
        # Check if the database engine is available
        if engine:
            # Set default start and end dates
            start_date = '2024-01-01'
            end_date = date.today()
            # Update start and end dates if a date range is provided
            if date_range:
                start_date, end_date = date_range
                
            # SQL query to filter orders based on the defined criteria
            filter_query = f""" 
                SELECT o.order_id, o.total_amount, DATE(o.order_date) order_date, o.customer_id, c.customer_name
                FROM orders o
                LEFT JOIN customers c
                ON o.customer_id=c.customer_id
                WHERE   (o.order_date BETWEEN '{start_date}' AND '{end_date}') AND
                        (c.customer_id IN ( SELECT customer_id
                                            FROM orders
                                            GROUP BY customer_id
                                            HAVING SUM(total_amount) > {min_amount} AND COUNT(order_id) > {min_orders}));
            """
            # Execute the SQL query and return the results as a DataFrame
            orders_df = pd.read_sql(filter_query, con=engine)
            return orders_df # Return the filtered DataFrame
        return st.error("Database connection error!") # Handle database connection error
    except Exception:
        return st.warning("something went wrong on filtering!") # Handle general errors

def filter_customer_by_amount(min_amount= 0, min_orders = 0):
    """
    Filter Customers Based on Spending and Order Count.

    This function filters customers based on their total spending and the number 
    of orders they have placed.

    Parameters:
        min_amount (float): The minimum amount spent by customers for filtering (default is 0).
        min_orders (int): The minimum number of orders placed by customers for filtering (default is 0).

    Returns:
        DataFrame: A DataFrame containing filtered customers.
    Raises:
        Exception: If there is an error during database interaction.
    """
    try:
        # Check if the database engine is available
        if engine:
            # SQL query to filter customers based on spending and order count
            filter_query = f"""
                SELECT c.customer_id, c.customer_name, sum_tab.total_spent,sum_tab.number_of_orders, c.customer_email 
                FROM customers c
                JOIN    (SELECT customer_id, SUM(total_amount) total_spent, COUNT(order_id) number_of_orders
                        FROM orders
                        GROUP BY customer_id
                        HAVING SUM(total_amount) > {min_amount} AND count(order_id) > {min_orders}) sum_tab
                ON c.customer_id = sum_tab.customer_id
            """
            # Execute the SQL query and return the results as a DataFrame
            customers_df = pd.read_sql(filter_query, con=engine)
            return customers_df # Return the filtered DataFrame
        return st.error("Database connection error!") # Handle database connection error
    except Exception:
        return st.warning("something went wrong on filtering!") # Handle general errors

def top_customer_by_revenue(top_number=10):
    """
    Retrieve Top Customers by Revenue.

    This function retrieves the top customers based on their total revenue from orders.

    Parameters:
        top_number (int): The number of top customers to retrieve (default is 10).

    Returns:
        DataFrame: A DataFrame containing top customers by revenue.
    Raises:
        Exception: If there is an error during database interaction.
    """
    try:
        # Check if the database engine is available
        if engine:
            # SQL query to retrieve top customers based on total revenue
            filter_query = f"""
                SELECT c.customer_id, c.customer_name, sum_tab.spent_amount, sum_tab.order_count
                FROM customers c
                RIGHT JOIN (SELECT customer_id, SUM(total_amount) spent_amount, COUNT(order_id) order_count
                            FROM orders
                            GROUP BY customer_id
                            ORDER BY spent_amount DESC
                            LIMIT {int(top_number)}) sum_tab
                ON c.customer_id=sum_tab.customer_id;
            """
            # Execute the SQL query and return the results as a DataFrame
            customers_df = pd.read_sql(filter_query, con=engine)
            return customers_df # Return the top customers DataFrame
        return st.error("Database connection error!") # Handle database connection error
    except Exception:
        return st.warning("something went wrong on filtering!") # Handle general errors

def get_total_over_time():
    """
    Get Revenue Data Grouped by Year and Month.

    This function fetches total revenue data grouped by year and month.

    Returns:
        DataFrame: A DataFrame containing revenue data over time.
    Raises:
        Exception: If there is an error during database interaction.
    """
    try:
        # Check if the database engine is available
        if engine:
            # SQL query to get revenue data grouped by year and month
            filter_query = f"""
                SELECT YEAR(order_date) order_year, MONTH(order_date) order_month, SUM(total_amount) spent_amount, COUNT(order_id) order_count
                FROM orders
                GROUP BY YEAR(order_date), MONTH(order_date)
                ORDER BY YEAR(order_date), MONTH(order_date)
            """
            # Execute the SQL query and return the results as a DataFrame
            revenue_df = pd.read_sql(filter_query, con=engine)
            return revenue_df # Return the revenue data DataFrame
        return st.error("Database connection error!") # Handle database connection error
    except Exception:
        return st.warning("something went wrong on filtering!") # Handle general error

def get_total_summery():
    """
    Get Summary Metrics for Total Revenue, Customers, and Orders.

    This function retrieves summary metrics for total revenue, unique customers, 
    and order counts.

    Returns:
        tuple: Total revenue, total customers, and total orders.
    Raises:
        Exception: If there is an error during database interaction.
    """
    try:
        # Check if the database engine is available
        if engine:
            # SQL query to count unique customers
            customer_query = "SELECT COUNT(DISTINCT(customer_id)) customer_count FROM customers;"
            # SQL query to get total order count and total revenue
            order_query = "SELECT COUNT(order_id) order_count, SUM(total_amount) total_spent FROM orders;"
            
            # Execute the customer query and store the result in a DataFrame
            customer_summery = pd.read_sql(customer_query, con=engine)
            # Execute the order query and store the result in a DataFrame
            order_summery = pd.read_sql(order_query, con=engine)
            
            # Retrieve the total count of customers, total revenue, and order count
            total_customers = int(customer_summery['customer_count'])
            total_revenue = float(order_summery['total_spent'])
            total_orders = int(order_summery['order_count'])
            
            # Return a tuple containing the summary metrics
            return total_revenue, total_customers, total_orders
        
        return st.error("Database connection error!")
    except Exception:
        return st.warning("something went wrong on filtering!")